"""
ProductRecommendation ORM model.
Represents suggested protection products linked to recommendations.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class ProductRecommendation(Base):
    """
    ProductRecommendation model - represents product suggestions.

    Attributes:
        id: Primary key
        recommendation_id: Foreign key to Recommendation
        product_name: Name of the suggested product (e.g., 'N95 Mask')
        product_type: Type of product (e.g., 'mask', 'respirator', 'air_purifier')
        product_url: Optional URL for more information

    Relationships:
        recommendation: The recommendation this product is linked to
    """

    __tablename__ = "product_recommendation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(Integer, ForeignKey("recommendation.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    product_type = Column(String(100), nullable=False)
    product_url = Column(String(500), nullable=True)

    # Relationships
    recommendation = relationship("Recommendation", back_populates="products")

    def __repr__(self):
        return f"<ProductRecommendation(id={self.id}, product_name='{self.product_name}')>"

