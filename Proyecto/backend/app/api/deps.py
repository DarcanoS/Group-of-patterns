"""
FastAPI dependencies.
Provides common dependencies for endpoints like database session and current user.
"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_token
from app.repositories.user_repository import UserRepository
from app.models.user import AppUser
from app.core.logging_config import logger

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> AppUser:
    """
    Get current authenticated user from JWT token.

    Args:
        token: JWT access token from Authorization header
        db: Database session

    Returns:
        Current user object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token
    payload = verify_token(token)
    if payload is None:
        logger.warning("Invalid token provided")
        raise credentials_exception

    # Extract user ID from token
    user_id_str: Optional[str] = payload.get("sub")
    if user_id_str is None:
        logger.warning("Token missing 'sub' claim")
        raise credentials_exception

    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.warning(f"Invalid user_id in token: {user_id_str}")
        raise credentials_exception

    # Get user from database
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if user is None:
        logger.warning(f"User not found: {user_id}")
        raise credentials_exception

    return user


def get_current_admin(
    current_user: AppUser = Depends(get_current_user)
) -> AppUser:
    """
    Verify that current user has Admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user (if admin)

    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.role or current_user.role.name != "Admin":
        logger.warning(f"Non-admin user attempted admin action: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    return current_user


def get_current_researcher_or_admin(
    current_user: AppUser = Depends(get_current_user)
) -> AppUser:
    """
    Verify that current user has Researcher or Admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user (if researcher or admin)

    Raises:
        HTTPException: If user is not a researcher or admin
    """
    if not current_user.role or current_user.role.name not in ["Researcher", "Admin"]:
        logger.warning(f"Unauthorized user attempted researcher action: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Researcher or Admin privileges required"
        )

    return current_user


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[AppUser]:
    """
    Get current user if authenticated, otherwise return None.
    Useful for endpoints that work for both authenticated and anonymous users.

    Args:
        token: Optional JWT access token
        db: Database session

    Returns:
        Current user object or None
    """
    if not token:
        return None

    try:
        return get_current_user(token, db)
    except HTTPException:
        return None

