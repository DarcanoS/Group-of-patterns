"""
Settings related Pydantic schemas (NoSQL-backed).
"""

from pydantic import BaseModel
from typing import Dict, Any, Optional


class UserPreferences(BaseModel):
    """Schema for user preferences (stored in NoSQL)."""
    user_id: int
    theme: str = "light"
    language: str = "en"
    notifications_enabled: bool = True
    default_location: Optional[str] = None
    favorite_stations: list[int] = []


class DashboardConfig(BaseModel):
    """Schema for dashboard configuration (stored in NoSQL)."""
    user_id: int
    widgets: list[Dict[str, Any]] = []
    layout: str = "default"
    refresh_interval: int = 300  # seconds


class SettingsUpdateRequest(BaseModel):
    """Schema for updating settings."""
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    default_location: Optional[str] = None
    favorite_stations: Optional[list[int]] = None

