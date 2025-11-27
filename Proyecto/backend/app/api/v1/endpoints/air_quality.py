"""
Air quality endpoints.
Uses Builder and Strategy patterns.
"""

from typing import Optional, List
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.air_quality_service import AirQualityService
from app.schemas.air_quality import CurrentAQIResponse, DailyStatsResponse, HistoricalDataResponse
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


@router.get("/historical/7-days", response_model=HistoricalDataResponse)
def get_7_day_historical_data(
    station_id: int = Query(..., description="Station ID to get historical data for"),
    end_date: Optional[date] = Query(None, description="End date (defaults to today)"),
    db: Session = Depends(get_db)
):
    """
    Get 7-day historical data for all pollutants at a specific station.

    Returns daily average values for all pollutants in the same date range,
    allowing for easy comparison in a single chart.

    Args:
        station_id: The station ID to get data for
        end_date: The end date of the range (defaults to today)

    Returns:
        Historical data organized by pollutant with daily data points
    """
    air_quality_service = AirQualityService(db)

    # Set end_date to today if not provided
    if end_date is None:
        end_date = date.today()

    # Calculate start_date (7 days before end_date)
    start_date = end_date - timedelta(days=6)

    result = air_quality_service.get_7_day_historical_data(
        station_id=station_id,
        start_date=start_date,
        end_date=end_date
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with ID {station_id} not found"
        )

    return result


