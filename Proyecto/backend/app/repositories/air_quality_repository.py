"""
Air quality repository for database operations.
Handles queries for air quality readings and daily statistics.
"""

from typing import Optional, List
from datetime import datetime, date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from app.models.air_quality_reading import AirQualityReading
from app.models.daily_stats import AirQualityDailyStats
from app.models.pollutant import Pollutant
from app.models.station import Station


class AirQualityRepository:
    """Repository for AirQuality-related database operations."""

    def __init__(self, db: Session):
        """
        Initialize AirQualityRepository.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_latest_reading_by_station(self, station_id: int) -> List[AirQualityReading]:
        """
        Get the most recent reading per pollutant for a station.

        Args:
            station_id: Station ID

        Returns:
            List of latest readings per pollutant
        """
        # Subquery to get the latest datetime per pollutant for this station
        subquery = (
            self.db.query(
                AirQualityReading.pollutant_id,
                func.max(AirQualityReading.datetime).label('max_datetime')
            )
            .filter(AirQualityReading.station_id == station_id)
            .group_by(AirQualityReading.pollutant_id)
            .subquery()
        )

        # Join to get the full readings
        readings = (
            self.db.query(AirQualityReading)
            .join(
                subquery,
                (AirQualityReading.pollutant_id == subquery.c.pollutant_id) &
                (AirQualityReading.datetime == subquery.c.max_datetime)
            )
            .filter(AirQualityReading.station_id == station_id)
            .options(joinedload(AirQualityReading.pollutant))
            .all()
        )

        return readings

    def get_latest_reading_by_city(self, city: str) -> Optional[List[AirQualityReading]]:
        """
        Get the most recent readings for stations in a city.

        Args:
            city: City name

        Returns:
            List of latest readings or None
        """
        # Get first station in the city
        station = self.db.query(Station).filter(Station.city.ilike(f"%{city}%")).first()

        if not station:
            return None

        return self.get_latest_reading_by_station(station.id)

    def get_readings_by_station(self, station_id: int, start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None,
                                pollutant_id: Optional[int] = None,
                                skip: int = 0, limit: int = 100) -> List[AirQualityReading]:
        """
        Get air quality readings with filters.

        Args:
            station_id: Station ID
            start_date: Start datetime filter
            end_date: End datetime filter
            pollutant_id: Pollutant ID filter
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of readings
        """
        query = self.db.query(AirQualityReading).filter(AirQualityReading.station_id == station_id)

        if start_date:
            query = query.filter(AirQualityReading.datetime >= start_date)
        if end_date:
            query = query.filter(AirQualityReading.datetime <= end_date)
        if pollutant_id:
            query = query.filter(AirQualityReading.pollutant_id == pollutant_id)

        return query.order_by(desc(AirQualityReading.datetime)).offset(skip).limit(limit).all()

    def get_daily_stats(self, station_id: Optional[int] = None,
                       pollutant_id: Optional[int] = None,
                       start_date: Optional[date] = None,
                       end_date: Optional[date] = None,
                       skip: int = 0, limit: int = 100) -> List[AirQualityDailyStats]:
        """
        Get daily statistics with filters.

        Args:
            station_id: Station ID filter
            pollutant_id: Pollutant ID filter
            start_date: Start date filter
            end_date: End date filter
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of daily statistics
        """
        query = self.db.query(AirQualityDailyStats)

        if station_id:
            query = query.filter(AirQualityDailyStats.station_id == station_id)
        if pollutant_id:
            query = query.filter(AirQualityDailyStats.pollutant_id == pollutant_id)
        if start_date:
            query = query.filter(AirQualityDailyStats.date >= start_date)
        if end_date:
            query = query.filter(AirQualityDailyStats.date <= end_date)

        return query.order_by(desc(AirQualityDailyStats.date)).offset(skip).limit(limit).all()

    def get_max_aqi_for_station(self, station_id: int) -> Optional[int]:
        """
        Get the maximum AQI from latest readings for a station.

        Args:
            station_id: Station ID

        Returns:
            Maximum AQI value or None
        """
        readings = self.get_latest_reading_by_station(station_id)
        if not readings:
            return None

        max_aqi = max((r.aqi for r in readings if r.aqi is not None), default=None)
        return max_aqi

