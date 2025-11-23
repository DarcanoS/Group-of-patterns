"""
API v1 router.
Includes all endpoint routers.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    stations,
    air_quality,
    recommendations,
    admin,
    settings,
    reports
)

api_router = APIRouter()

# Authentication
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Stations
api_router.include_router(
    stations.router,
    prefix="/stations",
    tags=["Stations"]
)

# Air Quality
api_router.include_router(
    air_quality.router,
    prefix="/air-quality",
    tags=["Air Quality"]
)

# Recommendations
api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recommendations"]
)

# Admin
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)

# Settings
api_router.include_router(
    settings.router,
    prefix="/settings",
    tags=["Settings"]
)

# Reports
api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"]
)

