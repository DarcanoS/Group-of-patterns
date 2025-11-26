"""
Alert repository for database operations.
Handles CRUD operations for Alert model.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.alert import Alert


class AlertRepository:
    """Repository for Alert-related database operations."""

    def __init__(self, db: Session):
        """
        Initialize AlertRepository.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, alert_id: int) -> Optional[Alert]:
        """
        Get alert by ID.

        Args:
            alert_id: Alert ID

        Returns:
            Alert object or None
        """
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def get_by_user(self, user_id: int) -> List[Alert]:
        """
        Get all alerts for a user.

        Args:
            user_id: User ID

        Returns:
            List of alerts
        """
        return self.db.query(Alert).filter(Alert.user_id == user_id).all()

    def create(self, user_id: int, pollutant_id: int, threshold: float, method: str) -> Alert:
        """
        Create a new alert.

        Args:
            user_id: User ID
            pollutant_id: Pollutant ID to monitor
            threshold: Threshold value to trigger alert
            method: Alert method (e.g., 'email', 'sms')

        Returns:
            Created alert object
        """
        alert = Alert(
            user_id=user_id,
            pollutant_id=pollutant_id,
            threshold=threshold,
            method=method
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def update(self, alert_id: int, **kwargs) -> Optional[Alert]:
        """
        Update alert information.

        Args:
            alert_id: Alert ID
            **kwargs: Fields to update

        Returns:
            Updated alert object or None
        """
        alert = self.get_by_id(alert_id)
        if not alert:
            return None

        for key, value in kwargs.items():
            if hasattr(alert, key) and value is not None:
                setattr(alert, key, value)

        self.db.commit()
        self.db.refresh(alert)
        return alert

    def trigger_alert(self, alert_id: int) -> Optional[Alert]:
        """
        Mark alert as triggered.

        Args:
            alert_id: Alert ID

        Returns:
            Updated alert object or None
        """
        return self.update(alert_id, triggered_at=datetime.utcnow())

    def delete(self, alert_id: int) -> bool:
        """
        Delete an alert.

        Args:
            alert_id: Alert ID

        Returns:
            True if deleted, False otherwise
        """
        alert = self.get_by_id(alert_id)
        if not alert:
            return False

        self.db.delete(alert)
        self.db.commit()
        return True

