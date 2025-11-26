"""
Admin endpoints.
Requires admin role.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_admin
from app.repositories.station_repository import StationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.station import StationResponse, StationCreate, StationUpdate
from app.schemas.user import UserResponse, UserUpdateRole
from app.schemas.common import MessageResponse, HealthCheckResponse
from app.models.user import AppUser
from app.models.pollutant import Pollutant
from app.core.logging_config import logger

router = APIRouter()


# Health check endpoint
@router.get("/health", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(get_db)):
    """
    Check API and database health.

    Returns status of the API and database connection.
    """
    try:
        # Try a simple query to check database connectivity
        pollutant_count = db.query(Pollutant).count()

        return HealthCheckResponse(
            status="healthy",
            database="connected",
            message=f"Database contains {pollutant_count} pollutants"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            database="error",
            message=str(e)
        )


# Station management endpoints
@router.get("/stations", response_model=List[StationResponse])
def list_stations_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_admin: AppUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    List all stations (admin only).
    """
    station_repo = StationRepository(db)
    stations = station_repo.get_all(skip=skip, limit=limit)

    return [StationResponse.model_validate(s) for s in stations]


@router.post("/stations", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
def create_station(
    station_data: StationCreate,
    current_admin: AppUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new monitoring station (admin only).
    """
    station_repo = StationRepository(db)

    station = station_repo.create(
        name=station_data.name,
        latitude=station_data.latitude,
        longitude=station_data.longitude,
        city=station_data.city,
        country=station_data.country,
        region_id=station_data.region_id
    )

    logger.info(f"Station created by admin {current_admin.id}: {station.id}")

    return StationResponse.model_validate(station)


@router.put("/stations/{station_id}", response_model=StationResponse)
def update_station(
    station_id: int,
    station_data: StationUpdate,
    current_admin: AppUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update a monitoring station (admin only).
    """
    station_repo = StationRepository(db)

    # Convert Pydantic model to dict, excluding unset fields
    update_data = station_data.model_dump(exclude_unset=True)

    station = station_repo.update(station_id, **update_data)

    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found"
        )

    logger.info(f"Station updated by admin {current_admin.id}: {station_id}")

    return StationResponse.model_validate(station)


@router.delete("/stations/{station_id}", response_model=MessageResponse)
def delete_station(
    station_id: int,
    current_admin: AppUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete a monitoring station (admin only).
    """
    station_repo = StationRepository(db)

    success = station_repo.delete(station_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found"
        )

    logger.info(f"Station deleted by admin {current_admin.id}: {station_id}")

    return MessageResponse(message=f"Station {station_id} deleted successfully")


# User management endpoints
@router.get("/users", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_admin: AppUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    List all users (admin only).
    """
    user_repo = UserRepository(db)
    users = user_repo.get_all(skip=skip, limit=limit)

    return [UserResponse.model_validate(u) for u in users]


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role_data: UserUpdateRole,
    current_admin: AppUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update a user's role (admin only).
    """
    user_repo = UserRepository(db)

    user = user_repo.update_role(user_id, role_data.role_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    logger.info(f"User role updated by admin {current_admin.id}: user={user_id}, new_role={role_data.role_id}")

    return UserResponse.model_validate(user)

