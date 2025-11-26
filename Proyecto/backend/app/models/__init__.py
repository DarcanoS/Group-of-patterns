"""
Models module initialization.
Import all ORM models here to ensure they are registered with SQLAlchemy Base.
"""

from app.models.pollutant import Pollutant
from app.models.region import MapRegion
from app.models.station import Station
from app.models.role import Role
from app.models.permission import Permission, role_permission
from app.models.user import AppUser
from app.models.air_quality_reading import AirQualityReading
from app.models.alert import Alert
from app.models.recommendation import Recommendation
from app.models.product_recommendation import ProductRecommendation
from app.models.report import Report
from app.models.daily_stats import AirQualityDailyStats

__all__ = [
    "Pollutant",
    "MapRegion",
    "Station",
    "Role",
    "Permission",
    "role_permission",
    "AppUser",
    "AirQualityReading",
    "Alert",
    "Recommendation",
    "ProductRecommendation",
    "Report",
    "AirQualityDailyStats",
]

