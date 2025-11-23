"""
User repository for database operations.
Handles CRUD operations for AppUser model.
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.models.user import AppUser
from app.models.role import Role
from app.core.security import get_password_hash


class UserRepository:
    """Repository for User-related database operations."""

    def __init__(self, db: Session):
        """
        Initialize UserRepository.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[AppUser]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        return self.db.query(AppUser).options(joinedload(AppUser.role)).filter(AppUser.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[AppUser]:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User object or None
        """
        return self.db.query(AppUser).options(joinedload(AppUser.role)).filter(AppUser.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AppUser]:
        """
        Get all users with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of users
        """
        return self.db.query(AppUser).options(joinedload(AppUser.role)).offset(skip).limit(limit).all()

    def create(self, name: str, email: str, password: str, role_id: int, location: Optional[str] = None) -> AppUser:
        """
        Create a new user.

        Args:
            name: User name
            email: User email
            password: Plain text password (will be hashed)
            role_id: Role ID
            location: User location (optional)

        Returns:
            Created user object
        """
        password_hash = get_password_hash(password)
        user = AppUser(
            name=name,
            email=email,
            password_hash=password_hash,
            role_id=role_id,
            location=location
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, **kwargs) -> Optional[AppUser]:
        """
        Update user information.

        Args:
            user_id: User ID
            **kwargs: Fields to update

        Returns:
            Updated user object or None
        """
        user = self.get_by_id(user_id)
        if not user:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def update_role(self, user_id: int, role_id: int) -> Optional[AppUser]:
        """
        Update user role.

        Args:
            user_id: User ID
            role_id: New role ID

        Returns:
            Updated user object or None
        """
        return self.update(user_id, role_id=role_id)

    def delete(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID

        Returns:
            True if deleted, False otherwise
        """
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True

