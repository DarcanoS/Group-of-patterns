"""
Air quality service.
Handles business logic for air quality data retrieval and analysis.
Uses Builder and Strategy patterns.
"""

from typing import Optional, List
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.repositories.air_quality_repository import AirQualityRepository
from app.repositories.station_repository import StationRepository
from app.services.risk_category import SimpleRiskCategoryStrategy, RiskCategory
from app.services.dashboard_service import DashboardResponseBuilder, DashboardResponseSchema
from app.schemas.air_quality import CurrentReadingResponse, DailyStatsResponse, StationResponse, CurrentAQIResponse
from app.schemas.pollutant import PollutantResponse
from app.core.logging_config import logger


class AirQualityService:
    """
    Service for air quality operations.
    Uses Strategy pattern for risk categorization and Builder pattern for responses.
    """

    def __init__(self, db: Session, risk_strategy: Optional[SimpleRiskCategoryStrategy] = None):
        """
        Initialize AirQualityService.

        Args:
            db: SQLAlchemy database session
            risk_strategy: Strategy for risk categorization (defaults to SimpleRiskCategoryStrategy)
        """
        self.db = db
        self.air_quality_repo = AirQualityRepository(db)
        self.station_repo = StationRepository(db)

        # STRATEGY PATTERN: Use pluggable strategy for risk categorization
        self.risk_strategy = risk_strategy or SimpleRiskCategoryStrategy()

    def get_current_aqi_for_city(self, city: str) -> Optional[CurrentAQIResponse]:
        """
        Get current AQI for a city.

        Args:
            city: City name

        Returns:
            CurrentAQIResponse or None
        """
        logger.info(f"Getting current AQI for city: {city}")

        # Get readings for the city
        readings = self.air_quality_repo.get_latest_reading_by_city(city)

        if not readings:
            logger.warning(f"No readings found for city: {city}")
            return None

        # Get the maximum AQI (dominant pollutant)
        max_aqi = max((r.aqi for r in readings if r.aqi is not None), default=0)
        dominant_reading = max(readings, key=lambda r: r.aqi or 0)

        # STRATEGY PATTERN: Use strategy to determine risk category
        risk_category = self.risk_strategy.get_category(max_aqi)

        # Get station info
        station = self.station_repo.get_by_id(dominant_reading.station_id)

        return CurrentAQIResponse(
            city=city,
            aqi=max_aqi,
            dominant_pollutant=dominant_reading.pollutant.name,
            category=risk_category.label,
            color=risk_category.color,
            health_message=risk_category.description,
            timestamp=dominant_reading.datetime,
            station=StationResponse.model_validate(station) if station else None
        )

    def get_station_current_readings(self, station_id: int) -> Optional[dict]:
        """
        Get current readings for a station.

        Args:
            station_id: Station ID

        Returns:
            Dictionary with station and readings
        """
        logger.info(f"Getting current readings for station: {station_id}")

        station = self.station_repo.get_by_id(station_id)
        if not station:
            logger.warning(f"Station not found: {station_id}")
            return None

        readings = self.air_quality_repo.get_latest_reading_by_station(station_id)

        # Convert to response schemas
        current_readings = [
            CurrentReadingResponse(
                pollutant=PollutantResponse.model_validate(r.pollutant),
                value=r.value,
                aqi=r.aqi,
                datetime=r.datetime
            )
            for r in readings
        ]

        return {
            "station": StationResponse.model_validate(station),
            "readings": current_readings
        }

    def get_dashboard_data(self, city: Optional[str] = None, station_id: Optional[int] = None) -> DashboardResponseSchema:
        """
        Get comprehensive dashboard data using Builder pattern.

        Args:
            city: City name (optional)
            station_id: Station ID (optional)

        Returns:
            DashboardResponseSchema with all dashboard data
        """
        logger.info(f"Building dashboard data for city={city}, station_id={station_id}")

        # BUILDER PATTERN: Use builder to construct complex response
        builder = DashboardResponseBuilder()

        # Determine station to use
        if station_id:
            station = self.station_repo.get_by_id(station_id)
        elif city:
            stations = self.station_repo.get_by_city(city)
            station = stations[0] if stations else None
        else:
            # Get first available station
            stations = self.station_repo.get_all(limit=1)
            station = stations[0] if stations else None

        if not station:
            logger.warning("No station found for dashboard data")
            return builder.with_metadata("error", "No station available").build()

        # Add station to builder
        builder.with_station(StationResponse.model_validate(station))

        # Get current readings
        readings = self.air_quality_repo.get_latest_reading_by_station(station.id)
        if readings:
            current_readings = [
                CurrentReadingResponse(
                    pollutant=PollutantResponse.model_validate(r.pollutant),
                    value=r.value,
                    aqi=r.aqi,
                    datetime=r.datetime
                )
                for r in readings
            ]
            builder.with_current_readings(current_readings)

            # Calculate overall AQI and get risk category
            max_aqi = max((r.aqi for r in readings if r.aqi is not None), default=0)
            if max_aqi > 0:
                builder.with_overall_aqi(max_aqi)
                # STRATEGY PATTERN: Get risk category
                risk_category = self.risk_strategy.get_category(max_aqi)
                builder.with_risk_category(risk_category)

        # Get daily stats (last 7 days)
        stats = self.air_quality_repo.get_daily_stats(
            station_id=station.id,
            limit=7
        )
        if stats:
            daily_stats = [DailyStatsResponse.model_validate(s) for s in stats]
            builder.with_daily_stats(daily_stats)

        return builder.build()

    def get_daily_stats(self, station_id: Optional[int] = None,
                       pollutant_id: Optional[int] = None,
                       start_date: Optional[date] = None,
                       end_date: Optional[date] = None,
                       skip: int = 0, limit: int = 100) -> List[DailyStatsResponse]:
        """
        Get daily statistics with filters.

        Args:
            station_id: Station ID filter
            pollutant_id: Pollutant ID filter
            start_date: Start date filter
            end_date: End date filter
            skip: Pagination skip
            limit: Pagination limit

        Returns:
            List of daily statistics
        """
        stats = self.air_quality_repo.get_daily_stats(
            station_id=station_id,
            pollutant_id=pollutant_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )

        return [DailyStatsResponse.model_validate(s) for s in stats]

