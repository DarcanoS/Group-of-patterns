"""
Common Pydantic schemas used across the application.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class ErrorResponse(BaseModel):
    """Generic error response."""
    detail: str


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    database: str
    message: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""
    skip: int = 0
    limit: int = 100

    model_config = ConfigDict(from_attributes=True)

