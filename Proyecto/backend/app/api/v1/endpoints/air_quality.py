"""
Air quality endpoints.
Uses Builder and Strategy patterns.
"""

from typing import Optional, List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.air_quality_service import AirQualityService
from app.schemas.air_quality import CurrentAQIResponse, DailyStatsResponse
from app.services.dashboard_service import DashboardResponseSchema

router = APIRouter()


@router.get("/current", response_model=CurrentAQIResponse)
def get_current_aqi(
    city: str = Query(..., description="City name to get AQI for"),
    db: Session = Depends(get_db)
):
    """
    Get current AQI for a city.

    Returns current air quality index with risk category and health recommendations.
    Uses Strategy pattern for risk categorization.
    """
    air_quality_service = AirQualityService(db)

    result = air_quality_service.get_current_aqi_for_city(city)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No air quality data found for city: {city}"
        )

    return result


@router.get("/dashboard", response_model=DashboardResponseSchema)
def get_dashboard_data(
    city: Optional[str] = Query(None, description="City name"),
    station_id: Optional[int] = Query(None, description="Station ID"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard data.

    Returns a complete dashboard response with:
    - Station information
    - Current readings
    - Daily statistics
    - Risk category (using Strategy pattern)

    Uses Builder pattern to construct the complex response.
    """
    air_quality_service = AirQualityService(db)

    dashboard_data = air_quality_service.get_dashboard_data(
        city=city,
        station_id=station_id
    )

    return dashboard_data


@router.get("/daily-stats", response_model=List[DailyStatsResponse])
def get_daily_stats(
    station_id: Optional[int] = Query(None, description="Filter by station ID"),
    pollutant_id: Optional[int] = Query(None, description="Filter by pollutant ID"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get daily air quality statistics with filters.

    Returns aggregated daily statistics for specified parameters.
    """
    air_quality_service = AirQualityService(db)

    stats = air_quality_service.get_daily_stats(
        station_id=station_id,
        pollutant_id=pollutant_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )

    return stats

