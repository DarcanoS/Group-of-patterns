"""
Alert related Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AlertBase(BaseModel):
    """Base alert schema."""
    pollutant_id: int
    threshold: float
    method: str  # 'email', 'sms', etc.


class AlertCreate(AlertBase):
    """Schema for creating an alert."""
    pass


class AlertUpdate(BaseModel):
    """Schema for updating an alert."""
    threshold: Optional[float] = None
    method: Optional[str] = None


class AlertResponse(AlertBase):
    """Schema for alert response."""
    id: int
    user_id: int
    triggered_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

