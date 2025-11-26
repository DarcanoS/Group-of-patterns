"""
AQICN API Adapter - Realtime Air Quality Data Provider

This adapter implements the Adapter pattern to integrate with the
AQICN (Air Quality Index China Network) API, which provides real-time
air quality data from monitoring stations worldwide.

API Documentation: https://aqicn.org/api/
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import requests
from requests.exceptions import RequestException, Timeout

from app.domain.dto import NormalizedReading
from app.providers.base_adapter import BaseExternalApiAdapter
from app.domain.normalization import (
    normalize_timestamp as convert_timestamp_to_utc
)

logger = logging.getLogger(__name__)


class AqicnApiAdapter(BaseExternalApiAdapter):
    """
    Adapter pattern implementation for AQICN API
    
    Fetches real-time air quality data from AQICN and normalizes it
    into the internal NormalizedReading format.
    
    Supports:
    - City-based queries (e.g., "bogota")
    - Geo-based queries (latitude, longitude)
    - Station search
    
    Design Pattern: Adapter
    Purpose: Unify different external API formats into a common internal format
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.waqi.info",
        timeout: int = 10
    ):
        """
        Initialize AQICN API adapter
        
        Args:
            api_key: AQICN API token
            base_url: Base URL for AQICN API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        logger.info(
            f"Initialized AqicnApiAdapter (base_url={base_url}, timeout={timeout}s)"
        )
    
    def fetch_readings(
        self,
        cities: Optional[List[str]] = None,
        coordinates: Optional[List[tuple]] = None
    ) -> List[NormalizedReading]:
        """
        Fetch and normalize readings from AQICN API
        
        Args:
            cities: List of city names to query (e.g., ["bogota", "medellin"])
            coordinates: List of (lat, lon) tuples to query
            
        Returns:
            List of NormalizedReading objects
        """
        all_readings = []
        
        # Fetch by city names
        if cities:
            for city in cities:
                try:
                    readings = self._fetch_city_feed(city)
                    all_readings.extend(readings)
                    logger.info(
                        f"Fetched {len(readings)} readings from city: {city}"
                    )
                except Exception as e:
                    logger.error(f"Failed to fetch data for city {city}: {e}")
        
        # Fetch by coordinates
        if coordinates:
            for lat, lon in coordinates:
                try:
                    readings = self._fetch_geo_feed(lat, lon)
                    all_readings.extend(readings)
                    logger.info(
                        f"Fetched {len(readings)} readings from coordinates: {lat}, {lon}"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to fetch data for coordinates ({lat}, {lon}): {e}"
                    )
        
        return all_readings
    
    def _fetch_city_feed(self, city: str) -> List[NormalizedReading]:
        """
        Fetch data for a specific city using city feed endpoint
        
        Endpoint: /feed/{city}/
        
        Args:
            city: City name (e.g., "bogota")
            
        Returns:
            List of NormalizedReading objects
        """
        url = f"{self.base_url}/feed/{city}/"
        params = {"token": self.api_key}
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "ok":
                logger.warning(
                    f"AQICN API error for city {city}: {data.get('data')}"
                )
                return []
            
            return self._parse_station_data(data.get("data", {}))
            
        except Timeout:
            logger.error(f"Timeout fetching data for city: {city}")
            return []
        except RequestException as e:
            logger.error(f"Request error for city {city}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching city {city}: {e}")
            return []
    
    def _fetch_geo_feed(self, lat: float, lon: float) -> List[NormalizedReading]:
        """
        Fetch data for nearest station to given coordinates
        
        Endpoint: /feed/geo:{lat};{lon}/
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            List of NormalizedReading objects
        """
        url = f"{self.base_url}/feed/geo:{lat};{lon}/"
        params = {"token": self.api_key}
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "ok":
                logger.warning(
                    f"AQICN API error for coordinates ({lat}, {lon}): {data.get('data')}"
                )
                return []
            
            return self._parse_station_data(data.get("data", {}))
            
        except Exception as e:
            logger.error(f"Error fetching geo feed ({lat}, {lon}): {e}")
            return []
    
    def search_stations(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search for stations by keyword
        
        Endpoint: /search/
        
        Args:
            keyword: Search keyword (e.g., "bogota")
            
        Returns:
            List of station information dictionaries
        """
        url = f"{self.base_url}/search/"
        params = {
            "token": self.api_key,
            "keyword": keyword
        }
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "ok":
                stations = data.get("data", [])
                logger.info(f"Found {len(stations)} stations for keyword: {keyword}")
                return stations
            else:
                logger.warning(f"Search failed for keyword {keyword}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching stations for keyword {keyword}: {e}")
            return []
    
    def _parse_station_data(self, station_data: Dict[str, Any]) -> List[NormalizedReading]:
        """
        Parse AQICN station data into NormalizedReading objects
        
        Args:
            station_data: Raw station data from AQICN API
            
        Returns:
            List of NormalizedReading objects (one per pollutant)
        """
        readings = []
        
        # Extract station information
        city_info = station_data.get("city", {})
        station_name_raw = city_info.get("name", "Unknown Station")
        
        geo = city_info.get("geo", [])
        latitude = float(geo[0]) if len(geo) > 0 else None
        longitude = float(geo[1]) if len(geo) > 1 else None
        
        # Extract city and country from name (e.g., "Carvajal, Bogota, Colombia")
        name_parts = [part.strip() for part in station_name_raw.split(',')]
        
        # Try to extract meaningful station name
        # AQICN format can be: "Station, City, Country" or "City, Country"
        if len(name_parts) >= 3:
            # Format: "Station, City, Country"
            station_name = name_parts[0]
            city = name_parts[1]
            country = name_parts[2]
        elif len(name_parts) == 2:
            # Format: "City, Country" - use city as station name
            station_name = name_parts[0]
            city = name_parts[0]
            country = name_parts[1]
        else:
            # Fallback
            station_name = station_name_raw
            city = "Unknown"
            country = "Unknown"
        
        # Clean up station name to match our database entries
        # Our DB has: "Carvajal", "Centro de Alto Rendimiento", "Las Ferias", etc.
        station_name_cleaned = self._clean_station_name(station_name)
        
        # External station ID
        external_station_id = str(station_data.get("idx", "unknown"))
        
        # Timestamp
        time_data = station_data.get("time", {})
        timestamp_str = time_data.get("iso")
        
        if timestamp_str:
            timestamp_utc = convert_timestamp_to_utc(timestamp_str)
        else:
            timestamp_utc = datetime.now(timezone.utc)
            logger.warning(f"No timestamp in data for station {station_name}, using current time")
        
        # Overall AQI (dominant pollutant)
        overall_aqi = station_data.get("aqi")
        if overall_aqi == "-":
            overall_aqi = None
        elif overall_aqi is not None:
            overall_aqi = int(overall_aqi)
        
        # Individual pollutant measurements (IAQI - Individual Air Quality Index)
        iaqi = station_data.get("iaqi", {})
        
        # Map AQICN pollutant codes to our standard names
        pollutant_mapping = {
            "pm25": "PM2.5",
            "pm10": "PM10",
            "o3": "O3",
            "no2": "NO2",
            "so2": "SO2",
            "co": "CO"
        }
        
        for aqicn_code, pollutant_name in pollutant_mapping.items():
            if aqicn_code in iaqi:
                pollutant_data = iaqi[aqicn_code]
                
                # AQICN provides AQI values directly (not concentrations)
                # The 'v' field is the AQI value
                aqi_value = pollutant_data.get("v")
                
                if aqi_value is None:
                    continue
                
                # For now, we store AQI as the value
                # TODO: Convert AQI back to concentration if needed
                value = float(aqi_value)
                
                # Determine unit based on pollutant
                if pollutant_name in ["PM2.5", "PM10"]:
                    unit = "µg/m³"
                elif pollutant_name == "CO":
                    unit = "ppm"
                else:  # O3, NO2, SO2
                    unit = "ppb"
                
                reading = NormalizedReading(
                    external_station_id=external_station_id,
                    station_name=station_name_cleaned,
                    latitude=latitude,
                    longitude=longitude,
                    city=city,
                    country=country,
                    pollutant_code=pollutant_name,
                    unit=unit,
                    value=value,
                    aqi=int(aqi_value),
                    timestamp_utc=timestamp_utc
                )
                
                readings.append(reading)
        
        if not readings:
            logger.warning(f"No valid pollutant readings found for station {station_name}")
        
        return readings
    
    def _clean_station_name(self, name: str) -> str:
        """
        Clean and normalize station name to match database entries.
        
        Maps AQICN station names to our database station names.
        
        Args:
            name: Raw station name from AQICN
            
        Returns:
            Cleaned station name
        """
        # Remove common suffixes and prefixes
        name = name.strip()
        
        # Direct mappings for known stations
        mappings = {
            "Carvajal - Sevillana": "Carvajal",
            "Carvajal-Sevillana": "Carvajal",
            "Centro de Alto Rendimiento": "Centro de Alto Rendimiento",
            "Las Ferias": "Las Ferias",
            "Puente Aranda": "Puente Aranda",
            "Suba": "Suba",
        }
        
        # Check for exact match
        for aqicn_name, db_name in mappings.items():
            if aqicn_name.lower() in name.lower() or name.lower() in aqicn_name.lower():
                logger.debug(f"Matched station: '{name}' -> '{db_name}'")
                return db_name
        
        # If no match, return cleaned name
        return name
    
    def __del__(self):
        """Close session on cleanup"""
        if hasattr(self, 'session'):
            self.session.close()
