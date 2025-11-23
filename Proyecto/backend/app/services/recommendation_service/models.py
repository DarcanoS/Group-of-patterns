"""
Factory Pattern - Models for recommendations.
"""

from typing import List, Optional
from pydantic import BaseModel


class ProductInfo(BaseModel):
    """Product information model."""
    name: str
    type: str  # 'mask', 'respirator', 'air_purifier', etc.
    url: Optional[str] = None


class BaseRecommendation(BaseModel):
    """
    Base recommendation model.

    This represents the interface for recommendations created by the factory.
    """
    pollution_level: int
    message: str
    category: str
    products: List[ProductInfo] = []
    actions: List[str] = []

