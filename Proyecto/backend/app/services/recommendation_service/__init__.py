"""
Recommendation service initialization.
"""

from app.services.recommendation_service.models import BaseRecommendation, ProductInfo
from app.services.recommendation_service.factory import RecommendationFactory

__all__ = [
    "BaseRecommendation",
    "ProductInfo",
    "RecommendationFactory",
]

