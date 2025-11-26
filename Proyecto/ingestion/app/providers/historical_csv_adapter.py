"""
Historical CSV data adapter.

Implements the Adapter pattern to read air quality data from CSV files
and convert it to the common NormalizedReading format.
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd

from app.domain.dto import NormalizedReading, StationMetadata
from app.domain.normalization import (
    standardize_pollutant_name,
    get_standard_unit,
    normalize_timestamp,
    is_valid_concentration,
    estimate_aqi
)
from app.logging_config import get_logger
from app.providers.base_adapter import BaseExternalApiAdapter

logger = get_logger(__name__)


class HistoricalCsvAdapter(BaseExternalApiAdapter):
    """
    **Adapter Pattern: CSV File Source**
    
    Adapts historical CSV air quality data files to the common
    NormalizedReading format used by the ingestion service.
    
    CSV format expected:
    - Header: date, pm25, pm10, o3, no2, so2, co
    - Date format: YYYY/M/D
    - Values: numeric or empty (missing data)
    """
    
    def __init__(
        self,
        csv_file_path: Path,
        station_metadata: StationMetadata,
        pollutant_mapping: Dict[str, Dict[str, str]]
    ):
        """
        Initialize the CSV adapter.
        
        Args:
            csv_file_path: Path to the CSV file
            station_metadata: Station metadata from configuration
            pollutant_mapping: Mapping of CSV columns to pollutant names/units
        """
        self.csv_file_path = csv_file_path
        self.station_metadata = station_metadata
        self.pollutant_mapping = pollutant_mapping
        
        logger.info(f"Initialized CSV adapter for: {csv_file_path.name}")
    
    def fetch_readings(self) -> List[NormalizedReading]:
        """
        Read CSV file and convert to NormalizedReading objects.
        
        Returns:
            List of normalized readings
        """
        logger.info(f"Reading CSV file: {self.csv_file_path}")
        
        if not self.csv_file_path.exists():
            logger.error(f"CSV file not found: {self.csv_file_path}")
            return []
        
        readings: List[NormalizedReading] = []
        
        try:
            # Read CSV using pandas for easier handling of missing values
            df = pd.read_csv(self.csv_file_path)
            
            # Clean column names (remove leading/trailing spaces)
            df.columns = df.columns.str.strip()
            
            logger.info(f"CSV loaded: {len(df)} rows, columns: {list(df.columns)}")
            
            # Process each row
            for idx, row in df.iterrows():
                row_readings = self._process_row(row, idx)
                readings.extend(row_readings)
            
            logger.info(
                f"✓ Processed {len(df)} rows from {self.csv_file_path.name}, "
                f"generated {len(readings)} valid readings"
            )
            
        except Exception as e:
            logger.error(f"Failed to read CSV file {self.csv_file_path}: {e}")
            raise
        
        return readings
    
    def _process_row(self, row: pd.Series, row_idx: int) -> List[NormalizedReading]:
        """
        Process a single CSV row and create NormalizedReading objects for each pollutant.
        
        Args:
            row: Pandas Series representing one CSV row
            row_idx: Row index (for logging)
            
        Returns:
            List of NormalizedReading objects (one per pollutant with valid data)
        """
        readings: List[NormalizedReading] = []
        
        # Extract timestamp
        try:
            date_str = str(row['date']).strip()
            timestamp_utc = normalize_timestamp(date_str)
        except Exception as e:
            logger.warning(f"Row {row_idx}: Invalid date '{row.get('date')}': {e}")
            return []
        
        # Process each pollutant column
        for csv_column, pollutant_info in self.pollutant_mapping.items():
            # Check if column exists in CSV
            if csv_column not in row:
                continue
            
            # Get raw value
            raw_value = row[csv_column]
            
            # Skip if missing (NaN, empty string, or whitespace)
            if pd.isna(raw_value) or str(raw_value).strip() == '':
                continue
            
            # Try to convert to float
            try:
                value = float(raw_value)
            except (ValueError, TypeError):
                logger.debug(
                    f"Row {row_idx}: Invalid value for {csv_column}: '{raw_value}'"
                )
                continue
            
            # Get pollutant metadata
            pollutant_name = pollutant_info['name']
            pollutant_code = standardize_pollutant_name(pollutant_name)
            unit = pollutant_info['unit']
            
            # Validate concentration
            if not is_valid_concentration(value, pollutant_code):
                logger.warning(
                    f"Row {row_idx}: Invalid concentration for {pollutant_code}: {value} {unit}"
                )
                continue
            
            # Estimate AQI if possible
            aqi = estimate_aqi(pollutant_code, value)
            
            # Create normalized reading
            try:
                reading = NormalizedReading(
                    external_station_id=self.station_metadata.station_code,
                    station_name=self.station_metadata.station_name,
                    latitude=self.station_metadata.latitude,
                    longitude=self.station_metadata.longitude,
                    city=self.station_metadata.city,
                    country=self.station_metadata.country,
                    pollutant_code=pollutant_code,
                    unit=unit,
                    value=value,
                    aqi=aqi,
                    timestamp_utc=timestamp_utc
                )
                
                readings.append(reading)
                
            except Exception as e:
                logger.warning(
                    f"Row {row_idx}: Failed to create NormalizedReading for "
                    f"{pollutant_code}: {e}"
                )
                continue
        
        return readings
    
    def __repr__(self) -> str:
        return f"<HistoricalCsvAdapter: {self.csv_file_path.name}>"
