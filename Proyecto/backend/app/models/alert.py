"""
Alert ORM model.
Represents user-configured alerts for pollution thresholds.
"""

from sqlalchemy import Column, Integer, Float, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base


class Alert(Base):
    """
    Alert model - represents user-configured pollution alerts.

    Attributes:
        id: Primary key
        user_id: Foreign key to AppUser
        pollutant_id: Foreign key to Pollutant
        threshold: AQI or value threshold that triggers the alert
        method: Notification method (e.g., 'email', 'sms', 'push')
        triggered_at: Timestamp when alert was last triggered

    Relationships:
        user: The user who configured this alert
        pollutant: The pollutant being monitored
    """

    __tablename__ = "alert"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("app_user.id"), nullable=False)
    pollutant_id = Column(Integer, ForeignKey("pollutant.id"), nullable=False)
    threshold = Column(Float, nullable=False)
    method = Column(String(50), nullable=False, default='email')
    triggered_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    user = relationship("AppUser", back_populates="alerts")
    pollutant = relationship("Pollutant", backref="alerts")

    def __repr__(self):
        return f"<Alert(id={self.id}, user_id={self.user_id}, threshold={self.threshold})>"

