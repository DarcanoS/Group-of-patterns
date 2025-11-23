"""
Pollutant related Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class PollutantBase(BaseModel):
    """Base pollutant schema."""
    name: str
    unit: str
    description: Optional[str] = None


class PollutantCreate(PollutantBase):
    """Schema for creating a pollutant."""
    pass


class PollutantResponse(PollutantBase):
    """Schema for pollutant response."""
    id: int

    model_config = ConfigDict(from_attributes=True)

