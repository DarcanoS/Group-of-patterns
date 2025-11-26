"""
Data normalization utilities.

Provides functions to:
- Convert timestamps to UTC
- Standardize pollutant names and codes
- Convert units
- Calculate AQI from raw pollutant values
- Validate data ranges
"""

from datetime import datetime, timezone
from typing import Optional, Dict
from dateutil import parser as date_parser

from app.logging_config import get_logger

logger = get_logger(__name__)


# ============================================================================
# Pollutant Name Standardization
# ============================================================================

POLLUTANT_NAME_MAPPING: Dict[str, str] = {
    # Particulate Matter
    "pm2.5": "PM2.5",
    "pm25": "PM2.5",
    "pm_2.5": "PM2.5",
    "pm10": "PM10",
    "pm_10": "PM10",
    
    # Gases
    "o3": "O3",
    "ozone": "O3",
    "no2": "NO2",
    "nitrogen_dioxide": "NO2",
    "so2": "SO2",
    "sulfur_dioxide": "SO2",
    "co": "CO",
    "carbon_monoxide": "CO",
}


def standardize_pollutant_name(raw_name: str) -> str:
    """
    Convert various pollutant name formats to standard names.
    
    Args:
        raw_name: Raw pollutant name from data source
        
    Returns:
        Standardized pollutant name (e.g., "PM2.5", "O3")
        
    Examples:
        >>> standardize_pollutant_name("pm25")
        "PM2.5"
        >>> standardize_pollutant_name("Ozone")
        "O3"
    """
    normalized = raw_name.strip().lower().replace(" ", "_")
    return POLLUTANT_NAME_MAPPING.get(normalized, raw_name.upper())


# ============================================================================
# Unit Standardization
# ============================================================================

STANDARD_UNITS: Dict[str, str] = {
    "PM2.5": "µg/m³",
    "PM10": "µg/m³",
    "O3": "ppb",
    "NO2": "ppb",
    "SO2": "ppb",
    "CO": "ppm",
}


def get_standard_unit(pollutant_code: str) -> str:
    """
    Get the standard unit for a given pollutant.
    
    Args:
        pollutant_code: Standardized pollutant code
        
    Returns:
        Standard unit string
    """
    return STANDARD_UNITS.get(pollutant_code, "unknown")


# ============================================================================
# Timestamp Normalization
# ============================================================================

def normalize_timestamp(timestamp_str: str, source_timezone: Optional[str] = None) -> datetime:
    """
    Convert timestamp string to UTC datetime.
    
    Args:
        timestamp_str: Timestamp string in various formats
        source_timezone: Source timezone name (e.g., "America/Bogota")
        
    Returns:
        Datetime object in UTC
        
    Examples:
        >>> normalize_timestamp("2019/10/2")
        datetime.datetime(2019, 10, 2, 0, 0, tzinfo=datetime.timezone.utc)
    """
    try:
        # Parse the timestamp
        dt = date_parser.parse(timestamp_str)
        
        # If no timezone info, assume source timezone or UTC
        if dt.tzinfo is None:
            if source_timezone:
                # TODO: Apply source timezone conversion if needed
                # For now, assume UTC for dates without time
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.replace(tzinfo=timezone.utc)
        
        # Convert to UTC
        dt_utc = dt.astimezone(timezone.utc)
        
        return dt_utc
    
    except Exception as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        raise ValueError(f"Invalid timestamp format: {timestamp_str}")


# ============================================================================
# Data Validation
# ============================================================================

def is_valid_concentration(value: float, pollutant_code: str) -> bool:
    """
    Check if a pollutant concentration value is within reasonable bounds.
    
    Args:
        value: Concentration value
        pollutant_code: Pollutant code
        
    Returns:
        True if value is valid, False otherwise
    """
    # Basic validation: non-negative
    if value < 0:
        return False
    
    # Upper bounds (very conservative, for catching obvious errors)
    MAX_VALUES = {
        "PM2.5": 1000,  # µg/m³
        "PM10": 2000,   # µg/m³
        "O3": 500,      # ppb
        "NO2": 500,     # ppb
        "SO2": 500,     # ppb
        "CO": 100,      # ppm
    }
    
    max_val = MAX_VALUES.get(pollutant_code, float('inf'))
    return value <= max_val


# ============================================================================
# AQI Calculation (Simplified)
# ============================================================================

def calculate_aqi_pm25(concentration: float) -> int:
    """
    Calculate AQI for PM2.5 (simplified US EPA formula).
    
    Args:
        concentration: PM2.5 concentration in µg/m³
        
    Returns:
        AQI value (0-500)
        
    Note:
        This is a simplified approximation. For production use,
        implement the full EPA AQI calculation with breakpoints.
    """
    # Simplified linear approximation
    # Real EPA AQI uses breakpoints and piecewise linear function
    
    if concentration <= 12.0:
        # Good (0-50)
        return int((50 / 12.0) * concentration)
    elif concentration <= 35.4:
        # Moderate (51-100)
        return int(51 + ((100 - 51) / (35.4 - 12.1)) * (concentration - 12.1))
    elif concentration <= 55.4:
        # Unhealthy for Sensitive Groups (101-150)
        return int(101 + ((150 - 101) / (55.4 - 35.5)) * (concentration - 35.5))
    elif concentration <= 150.4:
        # Unhealthy (151-200)
        return int(151 + ((200 - 151) / (150.4 - 55.5)) * (concentration - 55.5))
    elif concentration <= 250.4:
        # Very Unhealthy (201-300)
        return int(201 + ((300 - 201) / (250.4 - 150.5)) * (concentration - 150.5))
    else:
        # Hazardous (301-500)
        return int(301 + ((500 - 301) / (500.4 - 250.5)) * (concentration - 250.5))


def estimate_aqi(pollutant_code: str, value: float) -> Optional[int]:
    """
    Estimate AQI for a given pollutant and value.
    
    Args:
        pollutant_code: Standardized pollutant code
        value: Concentration value in standard units
        
    Returns:
        Estimated AQI value, or None if cannot be calculated
        
    Note:
        Currently only implements PM2.5 AQI calculation.
        Other pollutants return None and should be extended as needed.
    """
    if pollutant_code == "PM2.5":
        return calculate_aqi_pm25(value)
    
    # TODO: Implement AQI calculation for other pollutants
    # For now, return None for other pollutants
    return None
