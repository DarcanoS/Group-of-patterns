"""
Authentication related Pydantic schemas.
"""

from pydantic import BaseModel
from app.schemas.user import UserResponse


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: int
    email: str
    role: str


class LoginResponse(BaseModel):
    """Schema for login response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

