"""
User and authentication related Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# Role schemas
class RoleBase(BaseModel):
    """Base role schema."""
    name: str


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    pass


class RoleResponse(RoleBase):
    """Schema for role response."""
    id: int

    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    name: str
    email: EmailStr
    location: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str
    role_id: int = 1  # Default to Citizen role


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    name: Optional[str] = None
    location: Optional[str] = None


class UserUpdateRole(BaseModel):
    """Schema for updating user role (admin only)."""
    role_id: int


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    role_id: int
    role: Optional[RoleResponse] = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str

