"""
Builder Pattern - Dashboard response builder for complex responses.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.schemas.air_quality import CurrentReadingResponse, StationResponse, DailyStatsResponse
from app.schemas.recommendation import RecommendationResponse
from app.services.risk_category.interfaces import RiskCategory


class DashboardResponseSchema(BaseModel):
    """Complete dashboard response schema."""
    station: Optional[StationResponse] = None
    current_readings: List[CurrentReadingResponse] = []
    daily_stats: List[DailyStatsResponse] = []
    recommendation: Optional[Dict[str, Any]] = None
    risk_category: Optional[Dict[str, Any]] = None
    overall_aqi: Optional[int] = None
    timestamp: datetime = datetime.utcnow()
    metadata: Dict[str, Any] = {}


class DashboardResponseBuilder:
    """
    BUILDER PATTERN: Constructs complex dashboard responses step by step.

    This builder centralizes the construction of dashboard responses that combine
    data from multiple sources (stations, readings, stats, recommendations, risk categories).
    """

    def __init__(self):
        """Initialize the builder with an empty response."""
        self._response = DashboardResponseSchema()

    def with_station(self, station: StationResponse) -> 'DashboardResponseBuilder':
        """
        Add station information to the response.

        Args:
            station: Station data

        Returns:
            Self for method chaining
        """
        self._response.station = station
        return self

    def with_current_readings(self, readings: List[CurrentReadingResponse]) -> 'DashboardResponseBuilder':
        """
        Add current readings to the response.

        Args:
            readings: List of current readings

        Returns:
            Self for method chaining
        """
        self._response.current_readings = readings

        # Calculate overall AQI from readings
        if readings:
            aqi_values = [r.aqi for r in readings if r.aqi is not None]
            if aqi_values:
                self._response.overall_aqi = max(aqi_values)

        return self

    def with_daily_stats(self, stats: List[DailyStatsResponse]) -> 'DashboardResponseBuilder':
        """
        Add daily statistics to the response.

        Args:
            stats: List of daily statistics

        Returns:
            Self for method chaining
        """
        self._response.daily_stats = stats
        return self

    def with_recommendation(self, recommendation: Dict[str, Any]) -> 'DashboardResponseBuilder':
        """
        Add recommendation to the response.

        Args:
            recommendation: Recommendation data

        Returns:
            Self for method chaining
        """
        self._response.recommendation = recommendation
        return self

    def with_risk_category(self, risk_category: RiskCategory) -> 'DashboardResponseBuilder':
        """
        Add risk category to the response.

        Args:
            risk_category: Risk category object

        Returns:
            Self for method chaining
        """
        self._response.risk_category = risk_category.to_dict()
        return self

    def with_overall_aqi(self, aqi: int) -> 'DashboardResponseBuilder':
        """
        Explicitly set overall AQI.

        Args:
            aqi: Overall AQI value

        Returns:
            Self for method chaining
        """
        self._response.overall_aqi = aqi
        return self

    def with_metadata(self, key: str, value: Any) -> 'DashboardResponseBuilder':
        """
        Add metadata to the response.

        Args:
            key: Metadata key
            value: Metadata value

        Returns:
            Self for method chaining
        """
        self._response.metadata[key] = value
        return self

    def build(self) -> DashboardResponseSchema:
        """
        Build and return the final dashboard response.

        Returns:
            Complete DashboardResponseSchema object
        """
        # Update timestamp to current time
        self._response.timestamp = datetime.utcnow()

        # Validate that we have at least some data
        if not self._response.station and not self._response.current_readings:
            self.with_metadata("warning", "No station or reading data available")

        return self._response

    def reset(self) -> 'DashboardResponseBuilder':
        """
        Reset the builder to create a new response.

        Returns:
            Self with reset state
        """
        self._response = DashboardResponseSchema()
        return self

