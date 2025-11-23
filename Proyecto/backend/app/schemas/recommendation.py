"""
Recommendation related Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class ProductRecommendationBase(BaseModel):
    """Base product recommendation schema."""
    product_name: str
    product_type: str
    product_url: Optional[str] = None


class ProductRecommendationResponse(ProductRecommendationBase):
    """Schema for product recommendation response."""
    id: int
    recommendation_id: int

    model_config = ConfigDict(from_attributes=True)


class RecommendationBase(BaseModel):
    """Base recommendation schema."""
    location: str
    pollution_level: int
    message: str


class RecommendationCreate(RecommendationBase):
    """Schema for creating a recommendation."""
    user_id: int


class RecommendationResponse(RecommendationBase):
    """Schema for recommendation response."""
    id: int
    user_id: int
    created_at: datetime
    products: List[ProductRecommendationResponse] = []

    model_config = ConfigDict(from_attributes=True)


class RecommendationRequest(BaseModel):
    """Schema for requesting a recommendation."""
    location: Optional[str] = None
    aqi: Optional[int] = None

