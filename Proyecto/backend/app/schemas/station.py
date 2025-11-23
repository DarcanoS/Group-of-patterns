"""
Station related Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class StationBase(BaseModel):
    """Base station schema."""
    name: str
    latitude: float
    longitude: float
    city: str
    country: str
    region_id: Optional[int] = None


class StationCreate(StationBase):
    """Schema for creating a station."""
    pass


class StationUpdate(BaseModel):
    """Schema for updating a station."""
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    country: Optional[str] = None
    region_id: Optional[int] = None


class StationResponse(StationBase):
    """Schema for station response."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class RegionBase(BaseModel):
    """Base region schema."""
    name: str


class RegionResponse(RegionBase):
    """Schema for region response."""
    id: int

    model_config = ConfigDict(from_attributes=True)

