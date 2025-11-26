"""
Authentication service.
Handles user authentication and token management.
"""

from typing import Optional
from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.models.user import AppUser
from app.core.logging_config import logger


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: Session):
        """
        Initialize AuthService.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.user_repo = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> Optional[AppUser]:
        """
        Authenticate a user with email and password.

        Args:
            email: User email
            password: Plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.user_repo.get_by_email(email)

        if not user:
            logger.warning(f"Authentication failed: user not found for email {email}")
            return None

        if not verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: invalid password for email {email}")
            return None

        logger.info(f"User authenticated successfully: {email}")
        return user

    def create_token_for_user(self, user: AppUser) -> str:
        """
        Create an access token for a user.

        Args:
            user: User object

        Returns:
            JWT access token
        """
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.name if user.role else "Citizen"
        }

        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return access_token

    def login(self, email: str, password: str) -> Optional[dict]:
        """
        Complete login flow: authenticate and create token.

        Args:
            email: User email
            password: Plain text password

        Returns:
            Dictionary with access_token and user data, or None
        """
        user = self.authenticate_user(email, password)

        if not user:
            return None

        access_token = self.create_token_for_user(user)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

