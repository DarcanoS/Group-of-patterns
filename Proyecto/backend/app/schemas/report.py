"""
Report related Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional


class ReportBase(BaseModel):
    """Base report schema."""
    city: str
    start_date: date
    end_date: date
    station_id: Optional[int] = None
    pollutant_id: Optional[int] = None


class ReportCreate(ReportBase):
    """Schema for creating a report."""
    pass


class ReportResponse(ReportBase):
    """Schema for report response."""
    id: int
    user_id: int
    created_at: datetime
    file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

