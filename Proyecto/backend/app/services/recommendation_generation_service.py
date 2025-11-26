"""
Recommendation service using Factory pattern.
Generates personalized recommendations based on air quality data.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.air_quality_repository import AirQualityRepository
from app.repositories.user_repository import UserRepository
from app.services.recommendation_service import RecommendationFactory
from app.schemas.recommendation import RecommendationResponse
from app.models.user import AppUser
from app.core.logging_config import logger


class RecommendationService:
    """
    Service for recommendation operations.
    Uses Factory pattern to create personalized recommendations.
    """

    def __init__(self, db: Session):
        """
        Initialize RecommendationService.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.recommendation_repo = RecommendationRepository(db)
        self.air_quality_repo = AirQualityRepository(db)
        self.user_repo = UserRepository(db)

    def generate_current_recommendation(self, user: AppUser,
                                       location: Optional[str] = None,
                                       aqi: Optional[int] = None) -> RecommendationResponse:
        """
        Generate a recommendation for current conditions.
        Uses Factory pattern to create appropriate recommendation.

        Args:
            user: User object
            location: Location (city) for recommendation
            aqi: Optional explicit AQI value

        Returns:
            RecommendationResponse
        """
        logger.info(f"Generating recommendation for user {user.id}")

        # Determine location
        if not location:
            location = user.location or "your area"

        # Get current AQI if not provided
        if aqi is None:
            # Try to get AQI from user's location
            if user.location:
                readings = self.air_quality_repo.get_latest_reading_by_city(user.location)
                if readings:
                    aqi = max((r.aqi for r in readings if r.aqi is not None), default=50)
                else:
                    aqi = 50  # Default moderate value
            else:
                aqi = 50  # Default moderate value

        # FACTORY PATTERN: Create recommendation based on AQI and user role
        user_role = user.role.name if user.role else "Citizen"
        base_recommendation = RecommendationFactory.create_for_aqi(
            aqi=aqi,
            user_role=user_role,
            location=location
        )

        # Save to database
        recommendation = self.recommendation_repo.create(
            user_id=user.id,
            location=location,
            pollution_level=aqi,
            message=base_recommendation.message,
            created_at=datetime.utcnow()
        )

        # Add products to database
        for product in base_recommendation.products:
            self.recommendation_repo.add_product(
                recommendation_id=recommendation.id,
                product_name=product.name,
                product_type=product.type,
                product_url=product.url
            )

        # Reload to get products
        recommendation = self.recommendation_repo.get_by_id(recommendation.id)

        logger.info(f"Recommendation created: {recommendation.id}")

        return RecommendationResponse.model_validate(recommendation)

    def get_user_recommendation_history(self, user_id: int, skip: int = 0,
                                       limit: int = 100) -> List[RecommendationResponse]:
        """
        Get recommendation history for a user.

        Args:
            user_id: User ID
            skip: Pagination skip
            limit: Pagination limit

        Returns:
            List of recommendations
        """
        logger.info(f"Getting recommendation history for user {user_id}")

        recommendations = self.recommendation_repo.get_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit
        )

        return [RecommendationResponse.model_validate(r) for r in recommendations]

