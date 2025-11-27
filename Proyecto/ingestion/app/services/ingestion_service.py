"""
Ingestion service - Main orchestration logic.

Coordinates the ingestion process:
1. Load configuration (station mappings)
2. Initialize data source adapters
3. Fetch normalized readings
4. Map to database entities
5. Persist to database
"""

from pathlib import Path
from typing import List, Dict, Optional
import yaml

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.db.models import Station, Pollutant, AirQualityReading
from app.domain.dto import NormalizedReading, StationMetadata
from app.providers.base_adapter import BaseExternalApiAdapter
from app.providers.historical_csv_adapter import HistoricalCsvAdapter
from app.logging_config import get_logger

logger = get_logger(__name__)


class IngestionService:
    """
    Main ingestion orchestrator.
    
    Handles the complete ingestion workflow from data sources to database.
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize ingestion service.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        self.station_cache: Dict[str, int] = {}  # station_code -> station_id
        self.pollutant_cache: Dict[str, int] = {}  # pollutant_name -> pollutant_id
        
        logger.info("Ingestion service initialized")
    
    def load_station_mapping_config(self) -> Dict:
        """
        Load station mapping configuration from YAML file.
        
        Returns:
            Configuration dictionary
        """
        config_path = settings.get_station_mapping_path()
        
        logger.info(f"Loading station mapping from: {config_path}")
        
        if not config_path.exists():
            raise FileNotFoundError(f"Station mapping file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✓ Loaded mapping for {len(config.get('stations', []))} stations")
        
        return config
    
    def create_historical_adapters(self) -> List[BaseExternalApiAdapter]:
        """
        Create CSV adapters for all stations in the mapping configuration.
        
        Returns:
            List of HistoricalCsvAdapter instances
        """
        config = self.load_station_mapping_config()
        adapters: List[BaseExternalApiAdapter] = []
        
        data_dir = settings.get_historical_data_path()
        logger.info(f"Historical data directory: {data_dir}")
        
        stations_config = config.get('stations', [])
        pollutant_mapping = config.get('pollutant_mapping', {})
        
        for station_config in stations_config:
            csv_filename = station_config.get('csv_file')
            if not csv_filename:
                logger.warning(f"Station has no CSV file: {station_config.get('station_name')}")
                continue
            
            csv_path = data_dir / csv_filename
            
            # Create StationMetadata DTO
            station_metadata = StationMetadata(
                station_code=station_config['station_code'],
                station_name=station_config['station_name'],
                city=station_config['city'],
                country=station_config['country'],
                latitude=station_config['latitude'],
                longitude=station_config['longitude'],
                altitude=station_config.get('altitude'),
                address=station_config.get('address'),
                csv_file=csv_filename,
                geojson_file=station_config.get('geojson_file')
            )
            
            # Create adapter
            adapter = HistoricalCsvAdapter(
                csv_file_path=csv_path,
                station_metadata=station_metadata,
                pollutant_mapping=pollutant_mapping
            )
            
            adapters.append(adapter)
        
        logger.info(f"✓ Created {len(adapters)} CSV adapters")
        
        return adapters
    
    def run_historical_ingestion(self) -> Dict[str, int]:
        """
        Run the complete historical data ingestion process.
        
        Returns:
            Statistics dictionary with counts
        """
        logger.info("=" * 70)
        logger.info("Starting historical data ingestion")
        logger.info("=" * 70)
        
        stats = {
            'adapters_processed': 0,
            'readings_fetched': 0,
            'stations_created': 0,
            'stations_found': 0,
            'readings_inserted': 0,
            'readings_skipped': 0,
            'errors': 0
        }
        
        # Create adapters
        adapters = self.create_historical_adapters()
        
        # Process each adapter
        for adapter in adapters:
            try:
                logger.info(f"\n{'='*70}")
                logger.info(f"Processing: {adapter}")
                logger.info('='*70)
                
                # Fetch normalized readings
                readings = adapter.fetch_readings()
                stats['readings_fetched'] += len(readings)
                
                logger.info(f"Fetched {len(readings)} readings from CSV")
                
                # Persist to database
                logger.info("Persisting readings to database...")
                result = self._persist_readings(readings)
                stats['readings_inserted'] += result['inserted']
                stats['readings_skipped'] += result['skipped']
                
                # Summary for this adapter
                logger.info(f"\nAdapter Summary:")
                logger.info(f"  Total fetched: {len(readings)}")
                logger.info(f"  Inserted:      {result['inserted']}")
                logger.info(f"  Skipped:       {result['skipped']}")
                
                stats['adapters_processed'] += 1
                
            except Exception as e:
                logger.error(f"Error processing adapter {adapter}: {e}")
                stats['errors'] += 1
                continue
        
        # Final commit
        try:
            self.db.commit()
            logger.info("✓ Database transaction committed")
        except Exception as e:
            logger.error(f"Failed to commit transaction: {e}")
            self.db.rollback()
            raise
        
        # Log summary
        logger.info("\n" + "=" * 70)
        logger.info("Historical ingestion completed")
        logger.info("=" * 70)
        logger.info(f"Adapters processed: {stats['adapters_processed']}")
        logger.info(f"Readings fetched: {stats['readings_fetched']}")
        logger.info(f"Readings inserted: {stats['readings_inserted']}")
        logger.info(f"Readings skipped (duplicates): {stats['readings_skipped']}")
        logger.info(f"Errors: {stats['errors']}")
        logger.info("=" * 70)
        
        return stats
    
    def _persist_readings(self, readings: List[NormalizedReading]) -> Dict[str, int]:
        """
        Persist normalized readings to the database.
        
        Args:
            readings: List of normalized readings
            
        Returns:
            Dictionary with 'inserted' and 'skipped' counts
        """
        result = {'inserted': 0, 'skipped': 0}
        
        for reading in readings:
            try:
                # Get or create station
                station_id = self._get_or_create_station(reading)
                
                # Get pollutant ID
                pollutant_id = self._get_pollutant_id(reading.pollutant_code)
                
                if not pollutant_id:
                    logger.warning(
                        f"Pollutant '{reading.pollutant_code}' not found in database, skipping"
                    )
                    result['skipped'] += 1
                    continue
                
                # Check for duplicate
                existing = self.db.query(AirQualityReading).filter(
                    AirQualityReading.station_id == station_id,
                    AirQualityReading.pollutant_id == pollutant_id,
                    AirQualityReading.datetime == reading.timestamp_utc
                ).first()
                
                if existing:
                    # Skip duplicate
                    logger.debug(
                        f"⊘ DUPLICATE: {reading.station_name} | "
                        f"{reading.pollutant_code} | "
                        f"{reading.timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')} | "
                        f"Value: {reading.value:.2f} {reading.unit} | AQI: {reading.aqi}"
                    )
                    result['skipped'] += 1
                    continue
                
                # Create new reading
                db_reading = AirQualityReading(
                    station_id=station_id,
                    pollutant_id=pollutant_id,
                    datetime=reading.timestamp_utc,
                    value=reading.value,
                    aqi=reading.aqi
                )
                
                self.db.add(db_reading)
                result['inserted'] += 1
                
                # Log detailed information about inserted reading
                logger.info(
                    f"✓ INSERTED: {reading.station_name} | "
                    f"{reading.pollutant_code} | "
                    f"{reading.timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')} | "
                    f"Value: {reading.value:.2f} {reading.unit} | AQI: {reading.aqi}"
                )
                
            except Exception as e:
                logger.error(f"Failed to persist reading: {e}")
                result['skipped'] += 1
                continue
        
        # Flush to detect any constraint violations
        try:
            self.db.flush()
        except IntegrityError as e:
            logger.error(f"Integrity error during flush: {e}")
            self.db.rollback()
            raise
        
        return result
    
    def _get_or_create_station(self, reading: NormalizedReading) -> int:
        """
        Get existing station ID or create new station.
        
        Args:
            reading: Normalized reading with station metadata
            
        Returns:
            Station ID
        """
        station_code = reading.external_station_id
        
        # Check cache
        if station_code in self.station_cache:
            return self.station_cache[station_code]
        
        # Query database
        station = self.db.query(Station).filter(
            Station.name == reading.station_name
        ).first()
        
        if station:
            self.station_cache[station_code] = station.id
            logger.debug(f"Found existing station: {station.name} (ID: {station.id})")
            return station.id
        
        # Create new station
        logger.info(f"Creating new station: {reading.station_name}")
        
        new_station = Station(
            name=reading.station_name,
            latitude=reading.latitude,
            longitude=reading.longitude,
            city=reading.city,
            country=reading.country
        )
        
        self.db.add(new_station)
        self.db.flush()  # Get ID
        
        self.station_cache[station_code] = new_station.id
        logger.info(f"✓ Created station: {new_station.name} (ID: {new_station.id})")
        
        return new_station.id
    
    def _get_pollutant_id(self, pollutant_code: str) -> Optional[int]:
        """
        Get pollutant ID from database (uses cache).
        
        Args:
            pollutant_code: Standardized pollutant code
            
        Returns:
            Pollutant ID or None if not found
        """
        # Check cache
        if pollutant_code in self.pollutant_cache:
            return self.pollutant_cache[pollutant_code]
        
        # Query database
        pollutant = self.db.query(Pollutant).filter(
            Pollutant.name == pollutant_code
        ).first()
        
        if pollutant:
            self.pollutant_cache[pollutant_code] = pollutant.id
            return pollutant.id
        
        return None
    
    def preload_caches(self):
        """
        Preload station and pollutant caches from database.
        Improves performance by reducing database queries.
        """
        # Load all pollutants
        pollutants = self.db.query(Pollutant).all()
        for p in pollutants:
            self.pollutant_cache[p.name] = p.id
        
        logger.info(f"Preloaded {len(pollutants)} pollutants into cache")
        
        # Load existing stations
        stations = self.db.query(Station).all()
        for s in stations:
            # We don't have station_code in DB, so use name as key
            self.station_cache[s.name] = s.id
        
        logger.info(f"Preloaded {len(stations)} stations into cache")
    
    def run_aqicn_ingestion(self) -> Dict:
        """
        Run real-time ingestion from AQICN API.
        
        Fetches current air quality data from AQICN for stations that are
        already in our database, using their coordinates to query the API.
        
        Returns:
            Statistics dictionary with counts
        """
        from app.providers.aqicn_adapter import AqicnApiAdapter
        
        logger.info("=" * 70)
        logger.info("AQICN API INGESTION - UPDATE EXISTING STATIONS")
        logger.info("=" * 70)
        
        # Initialize AQICN adapter
        if not settings.aqicn_api_key:
            raise ValueError("AQICN_API_KEY not configured in environment")
        
        adapter = AqicnApiAdapter(
            api_key=settings.aqicn_api_key,
            base_url=settings.aqicn_base_url
        )
        
        # Get all stations from database
        logger.info("\n[1/4] Loading existing stations from database...")
        stations = self.db.query(Station).all()
        
        if not stations:
            logger.warning("No stations found in database!")
            return {
                'total_fetched': 0,
                'inserted': 0,
                'skipped': 0
            }
        
        logger.info(f"✓ Found {len(stations)} stations in database")
        
        # Prepare coordinates for each station
        coordinates = []
        station_info = {}
        
        for station in stations:
            if station.latitude and station.longitude:
                coord_tuple = (station.latitude, station.longitude)
                coordinates.append(coord_tuple)
                station_info[coord_tuple] = {
                    'id': station.id,
                    'name': station.name,
                    'city': station.city
                }
        
        logger.info(f"   Stations with valid coordinates: {len(coordinates)}")
        
        for coord in coordinates:
            info = station_info[coord]
            logger.info(f"   • {info['name']} ({info['city']}): {coord[0]:.4f}, {coord[1]:.4f}")
        
        # Fetch readings from AQICN for each station's coordinates
        logger.info("\n[2/4] Fetching current data from AQICN API...")
        
        readings = adapter.fetch_readings(coordinates=coordinates)
        
        logger.info(f"✓ Fetched {len(readings)} readings from AQICN")
        logger.info(f"✓ Fetched {len(readings)} readings from AQICN")
        
        # Persist to database
        logger.info("\n[3/4] Persisting readings to database...")
        result = self._persist_readings(readings)
        
        # Commit transaction
        logger.info("\n[4/4] Committing transaction...")
        self.db.commit()
        
        # Generate detailed summary by station
        logger.info("\n" + "=" * 70)
        logger.info("INGESTION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"  Stations queried:       {len(coordinates)}")
        logger.info(f"  Total readings fetched: {len(readings)}")
        logger.info(f"  Inserted:               {result['inserted']}")
        logger.info(f"  Skipped (duplicates):   {result['skipped']}")
        
        # Group readings by station for detailed summary
        if readings:
            logger.info("\n" + "-" * 70)
            logger.info("READINGS BY STATION")
            logger.info("-" * 70)
            
            # Group readings by station name
            from collections import defaultdict
            station_readings = defaultdict(list)
            for reading in readings:
                station_readings[reading.station_name].append(reading)
            
            for station_name, station_data in sorted(station_readings.items()):
                # Get unique timestamp (should be the same for all readings from same station)
                timestamp = station_data[0].timestamp_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
                
                logger.info(f"\n  📍 {station_name} ({station_data[0].city})")
                logger.info(f"     Timestamp: {timestamp}")
                logger.info(f"     Pollutants ({len(station_data)}):")
                
                for reading in sorted(station_data, key=lambda x: x.pollutant_code):
                    logger.info(
                        f"       • {reading.pollutant_code:<6} = "
                        f"{reading.value:>6.2f} {reading.unit:<6} "
                        f"(AQI: {reading.aqi:>3})"
                    )
        
        logger.info("\n" + "=" * 70)

        
        return {
            'stations_queried': len(coordinates),
            'total_fetched': len(readings),
            'inserted': result['inserted'],
            'skipped': result['skipped']
        }
