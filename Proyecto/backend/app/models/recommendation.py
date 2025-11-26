"""
Recommendation ORM model.
Represents personalized air quality recommendations for users.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base


class Recommendation(Base):
    """
    Recommendation model - represents personalized recommendations.

    Attributes:
        id: Primary key
        user_id: Foreign key to AppUser
        location: City or area name for which recommendation was generated
        pollution_level: AQI value used to determine the recommendation
        message: Human-readable recommendation text
        created_at: Timestamp when recommendation was created

    Relationships:
        user: The user who received this recommendation
        products: Suggested products for this recommendation
    """

    __tablename__ = "recommendation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("app_user.id"), nullable=False)
    location = Column(String(255), nullable=False)
    pollution_level = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    # Relationships
    user = relationship("AppUser", back_populates="recommendations")
    products = relationship("ProductRecommendation", back_populates="recommendation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Recommendation(id={self.id}, user_id={self.user_id}, pollution_level={self.pollution_level})>"

