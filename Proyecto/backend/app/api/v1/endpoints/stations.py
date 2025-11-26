"""
Station endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.repositories.station_repository import StationRepository
from app.schemas.station import StationResponse
from app.services.air_quality_service import AirQualityService
from app.schemas.air_quality import CurrentReadingResponse
from app.models.user import AppUser

router = APIRouter()


@router.get("", response_model=List[StationResponse])
def list_stations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    city: Optional[str] = None,
    country: Optional[str] = None,
    region_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    List all monitoring stations with optional filters.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **city**: Filter by city name (partial match)
    - **country**: Filter by country name (partial match)
    - **region_id**: Filter by region ID
    """
    station_repo = StationRepository(db)

    stations = station_repo.get_all(
        skip=skip,
        limit=limit,
        city=city,
        country=country,
        region_id=region_id
    )

    return [StationResponse.model_validate(s) for s in stations]


@router.get("/{station_id}", response_model=StationResponse)
def get_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific station by ID.
    """
    station_repo = StationRepository(db)
    station = station_repo.get_by_id(station_id)

    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found"
        )

    return StationResponse.model_validate(station)


@router.get("/{station_id}/readings/current")
def get_station_current_readings(
    station_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the most recent reading per pollutant for a station.

    Returns current air quality measurements from the station.
    """
    air_quality_service = AirQualityService(db)

    result = air_quality_service.get_station_current_readings(station_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found"
        )

    return result

