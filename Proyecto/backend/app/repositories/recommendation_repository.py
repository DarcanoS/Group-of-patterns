"""
Recommendation repository for database operations.
Handles CRUD operations for Recommendation and ProductRecommendation models.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from app.models.recommendation import Recommendation
from app.models.product_recommendation import ProductRecommendation


class RecommendationRepository:
    """Repository for Recommendation-related database operations."""

    def __init__(self, db: Session):
        """
        Initialize RecommendationRepository.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, recommendation_id: int) -> Optional[Recommendation]:
        """
        Get recommendation by ID.

        Args:
            recommendation_id: Recommendation ID

        Returns:
            Recommendation object or None
        """
        return self.db.query(Recommendation).options(
            joinedload(Recommendation.products)
        ).filter(Recommendation.id == recommendation_id).first()

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Recommendation]:
        """
        Get recommendations for a user.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of recommendations
        """
        return (
            self.db.query(Recommendation)
            .options(joinedload(Recommendation.products))
            .filter(Recommendation.user_id == user_id)
            .order_by(desc(Recommendation.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, user_id: int, location: str, pollution_level: int,
               message: str, created_at: datetime) -> Recommendation:
        """
        Create a new recommendation.

        Args:
            user_id: User ID
            location: Location (city) for the recommendation
            pollution_level: AQI value used
            message: Recommendation message
            created_at: Timestamp of creation

        Returns:
            Created recommendation object
        """
        recommendation = Recommendation(
            user_id=user_id,
            location=location,
            pollution_level=pollution_level,
            message=message,
            created_at=created_at
        )
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation

    def add_product(self, recommendation_id: int, product_name: str,
                   product_type: str, product_url: Optional[str] = None) -> ProductRecommendation:
        """
        Add a product recommendation.

        Args:
            recommendation_id: Recommendation ID
            product_name: Product name
            product_type: Product type (e.g., 'mask', 'respirator')
            product_url: Optional product URL

        Returns:
            Created product recommendation object
        """
        product = ProductRecommendation(
            recommendation_id=recommendation_id,
            product_name=product_name,
            product_type=product_type,
            product_url=product_url
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, recommendation_id: int) -> bool:
        """
        Delete a recommendation.

        Args:
            recommendation_id: Recommendation ID

        Returns:
            True if deleted, False otherwise
        """
        recommendation = self.get_by_id(recommendation_id)
        if not recommendation:
            return False

        self.db.delete(recommendation)
        self.db.commit()
        return True

