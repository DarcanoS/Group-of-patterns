"""
Schemas package initialization.
Import all schemas for easy access.
"""

from app.schemas.common import (
    MessageResponse,
    ErrorResponse,
    HealthCheckResponse,
    PaginationParams
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserUpdateRole,
    UserResponse,
    UserLogin,
    RoleBase,
    RoleCreate,
    RoleResponse
)
from app.schemas.auth import (
    Token,
    TokenData,
    LoginResponse
)
from app.schemas.station import (
    StationBase,
    StationCreate,
    StationUpdate,
    StationResponse,
    RegionBase,
    RegionResponse
)
from app.schemas.pollutant import (
    PollutantBase,
    PollutantCreate,
    PollutantResponse
)
from app.schemas.air_quality import (
    AirQualityReadingBase,
    AirQualityReadingResponse,
    CurrentReadingResponse,
    StationCurrentReadingsResponse,
    DailyStatsBase,
    DailyStatsResponse,
    CurrentAQIRequest,
    CurrentAQIResponse
)
from app.schemas.recommendation import (
    ProductRecommendationBase,
    ProductRecommendationResponse,
    RecommendationBase,
    RecommendationCreate,
    RecommendationResponse,
    RecommendationRequest
)
from app.schemas.report import (
    ReportBase,
    ReportCreate,
    ReportResponse
)
from app.schemas.settings import (
    UserPreferences,
    DashboardConfig,
    SettingsUpdateRequest
)
from app.schemas.alert import (
    AlertBase,
    AlertCreate,
    AlertUpdate,
    AlertResponse
)

__all__ = [
    "MessageResponse",
    "ErrorResponse",
    "HealthCheckResponse",
    "PaginationParams",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserUpdateRole",
    "UserResponse",
    "UserLogin",
    "RoleBase",
    "RoleCreate",
    "RoleResponse",
    "Token",
    "TokenData",
    "LoginResponse",
    "StationBase",
    "StationCreate",
    "StationUpdate",
    "StationResponse",
    "RegionBase",
    "RegionResponse",
    "PollutantBase",
    "PollutantCreate",
    "PollutantResponse",
    "AirQualityReadingBase",
    "AirQualityReadingResponse",
    "CurrentReadingResponse",
    "StationCurrentReadingsResponse",
    "DailyStatsBase",
    "DailyStatsResponse",
    "CurrentAQIRequest",
    "CurrentAQIResponse",
    "ProductRecommendationBase",
    "ProductRecommendationResponse",
    "RecommendationBase",
    "RecommendationCreate",
    "RecommendationResponse",
    "RecommendationRequest",
    "ReportBase",
    "ReportCreate",
    "ReportResponse",
    "UserPreferences",
    "DashboardConfig",
    "SettingsUpdateRequest",
    "AlertBase",
    "AlertCreate",
    "AlertUpdate",
    "AlertResponse",
]

