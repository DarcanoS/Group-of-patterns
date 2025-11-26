"""
Data Transfer Objects (DTOs) for the ingestion service.
These Pydantic models represent normalized air quality data.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class NormalizedReading(BaseModel):
    """
    Normalized air quality reading from any data source.
    
    This is the common format used internally by the ingestion service,
    regardless of whether data comes from CSV files or external APIs.
    """
    
    # Station identification (external or internal)
    external_station_id: str = Field(
        description="External station identifier (e.g., from CSV filename or API)"
    )
    station_name: Optional[str] = Field(
        default=None,
        description="Human-readable station name"
    )
    
    # Location data
    latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
        description="Station latitude in WGS84"
    )
    longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
        description="Station longitude in WGS84"
    )
    city: Optional[str] = Field(
        default=None,
        description="City name"
    )
    country: Optional[str] = Field(
        default=None,
        description="Country name"
    )
    
    # Pollutant data
    pollutant_code: str = Field(
        description="Standardized pollutant code (e.g., 'PM2.5', 'PM10', 'O3')"
    )
    unit: str = Field(
        description="Measurement unit (e.g., 'µg/m³', 'ppb', 'ppm')"
    )
    value: float = Field(
        description="Measured pollutant concentration"
    )
    
    # Air Quality Index
    aqi: Optional[int] = Field(
        default=None,
        ge=0,
        le=500,
        description="Air Quality Index (0-500, optional)"
    )
    
    # Timestamp
    timestamp_utc: datetime = Field(
        description="Measurement timestamp in UTC"
    )
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, v: float) -> float:
        """Ensure value is non-negative."""
        if v < 0:
            raise ValueError(f"Pollutant value cannot be negative: {v}")
        return v
    
    @field_validator('pollutant_code')
    @classmethod
    def normalize_pollutant_code(cls, v: str) -> str:
        """Normalize pollutant code to standard format."""
        # Convert to uppercase and remove whitespace
        return v.strip().upper()
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "external_station_id": "carvajal-bogota",
                "station_name": "Carvajal",
                "latitude": 4.614728,
                "longitude": -74.139465,
                "city": "Bogotá",
                "country": "Colombia",
                "pollutant_code": "PM2.5",
                "unit": "µg/m³",
                "value": 35.5,
                "aqi": 100,
                "timestamp_utc": "2025-11-26T12:00:00Z"
            }
        }


class StationMetadata(BaseModel):
    """
    Station metadata from configuration or external sources.
    """
    
    station_code: str = Field(description="Unique station code")
    station_name: str = Field(description="Station name")
    city: str = Field(description="City name")
    country: str = Field(description="Country name")
    latitude: float = Field(ge=-90, le=90, description="Latitude")
    longitude: float = Field(ge=-180, le=180, description="Longitude")
    altitude: Optional[int] = Field(default=None, description="Altitude in meters")
    address: Optional[str] = Field(default=None, description="Physical address")
    
    # File mappings for historical data
    csv_file: Optional[str] = Field(default=None, description="CSV data file name")
    geojson_file: Optional[str] = Field(default=None, description="GeoJSON metadata file name")
