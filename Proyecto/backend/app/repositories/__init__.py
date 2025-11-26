"""
Repository package initialization.
Import all repositories for easy access.
"""

from app.repositories.user_repository import UserRepository
from app.repositories.station_repository import StationRepository
from app.repositories.air_quality_repository import AirQualityRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.alert_repository import AlertRepository

__all__ = [
    "UserRepository",
    "StationRepository",
    "AirQualityRepository",
    "RecommendationRepository",
    "ReportRepository",
    "AlertRepository",
]

