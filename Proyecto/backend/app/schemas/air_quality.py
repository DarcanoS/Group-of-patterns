"""
Air quality reading and statistics related Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional, List
from app.schemas.pollutant import PollutantResponse
from app.schemas.station import StationResponse


class AirQualityReadingBase(BaseModel):
    """Base air quality reading schema."""
    station_id: int
    pollutant_id: int
    datetime: datetime
    value: float
    aqi: Optional[int] = None


class AirQualityReadingResponse(AirQualityReadingBase):
    """Schema for air quality reading response."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class CurrentReadingResponse(BaseModel):
    """Schema for current reading with pollutant details."""
    pollutant: PollutantResponse
    value: float
    aqi: Optional[int]
    datetime: datetime

    model_config = ConfigDict(from_attributes=True)


class StationCurrentReadingsResponse(BaseModel):
    """Schema for station with current readings."""
    station: StationResponse
    readings: List[CurrentReadingResponse]


class DailyStatsBase(BaseModel):
    """Base daily statistics schema."""
    station_id: int
    pollutant_id: int
    date: date
    avg_value: float
    avg_aqi: Optional[int] = None
    max_aqi: Optional[int] = None
    min_aqi: Optional[int] = None
    readings_count: int


class DailyStatsResponse(DailyStatsBase):
    """Schema for daily statistics response."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class CurrentAQIRequest(BaseModel):
    """Schema for requesting current AQI."""
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CurrentAQIResponse(BaseModel):
    """Schema for current AQI response."""
    city: str
    aqi: int
    dominant_pollutant: str
    category: str
    color: str
    health_message: str
    timestamp: datetime
    station: Optional[StationResponse] = None


class PollutantHistoricalData(BaseModel):
    """Schema for historical data of a single pollutant."""
    pollutant: PollutantResponse
    data_points: List[dict]  # [{date: str, value: float, aqi: int}]

    model_config = ConfigDict(from_attributes=True)


class HistoricalDataResponse(BaseModel):
    """Schema for 7-day historical data response."""
    station: StationResponse
    start_date: date
    end_date: date
    pollutants_data: List[PollutantHistoricalData]

    model_config = ConfigDict(from_attributes=True)


