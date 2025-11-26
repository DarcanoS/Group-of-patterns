"""
Recommendations endpoints.
Uses Factory pattern for generating recommendations.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.recommendation_generation_service import RecommendationService
from app.schemas.recommendation import RecommendationResponse, RecommendationRequest
from app.models.user import AppUser

router = APIRouter()


@router.get("/current", response_model=RecommendationResponse)
def get_current_recommendation(
    location: Optional[str] = Query(None, description="Location to get recommendation for"),
    aqi: Optional[int] = Query(None, description="Explicit AQI value to use"),
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a personalized recommendation for current conditions.

    Uses Factory pattern to create recommendations based on:
    - Current AQI levels
    - User role (Citizen, Researcher, Admin)
    - Location

    The recommendation is saved to the database and includes:
    - Health advice
    - Recommended actions
    - Product recommendations (masks, air purifiers, etc.)
    """
    recommendation_service = RecommendationService(db)

    recommendation = recommendation_service.generate_current_recommendation(
        user=current_user,
        location=location,
        aqi=aqi
    )

    return recommendation


@router.get("/history", response_model=List[RecommendationResponse])
def get_recommendation_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get recommendation history for the current user.

    Returns a paginated list of previous recommendations.
    """
    recommendation_service = RecommendationService(db)

    recommendations = recommendation_service.get_user_recommendation_history(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

    return recommendations

