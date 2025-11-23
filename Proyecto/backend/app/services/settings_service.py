"""
Settings service for user preferences and dashboard configurations.
Uses Prototype pattern for dashboard configs.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.services.dashboard_service import default_dashboard_prototype
from app.schemas.settings import UserPreferences, DashboardConfig
from app.core.logging_config import logger


class SettingsService:
    """
    Service for settings operations.
    Uses Prototype pattern for dashboard configurations.

    Note: This is a mock implementation. In production, this would connect
    to a NoSQL database (MongoDB/Redis) for flexible settings storage.
    """

    def __init__(self, db: Session):
        """
        Initialize SettingsService.

        Args:
            db: SQLAlchemy database session (for future SQL storage if needed)
        """
        self.db = db
        # Mock storage (in production, this would be NoSQL)
        self._preferences_store: Dict[int, UserPreferences] = {}
        self._dashboard_store: Dict[int, DashboardConfig] = {}

    def get_user_preferences(self, user_id: int) -> UserPreferences:
        """
        Get user preferences (mock implementation).

        Args:
            user_id: User ID

        Returns:
            UserPreferences object
        """
        logger.info(f"Getting preferences for user {user_id}")

        if user_id not in self._preferences_store:
            # Create default preferences
            self._preferences_store[user_id] = UserPreferences(user_id=user_id)

        return self._preferences_store[user_id]

    def update_user_preferences(self, user_id: int, **updates) -> UserPreferences:
        """
        Update user preferences.

        Args:
            user_id: User ID
            **updates: Fields to update

        Returns:
            Updated UserPreferences
        """
        logger.info(f"Updating preferences for user {user_id}")

        preferences = self.get_user_preferences(user_id)

        # Update fields
        for key, value in updates.items():
            if hasattr(preferences, key) and value is not None:
                setattr(preferences, key, value)

        self._preferences_store[user_id] = preferences

        return preferences

    def get_dashboard_config(self, user_id: int) -> DashboardConfig:
        """
        Get dashboard configuration for a user.
        Uses Prototype pattern to clone default config for new users.

        Args:
            user_id: User ID

        Returns:
            DashboardConfig object
        """
        logger.info(f"Getting dashboard config for user {user_id}")

        if user_id not in self._dashboard_store:
            # PROTOTYPE PATTERN: Clone default dashboard configuration
            default_config = default_dashboard_prototype.clone_for_user(user_id)

            self._dashboard_store[user_id] = DashboardConfig(
                user_id=user_id,
                widgets=default_config.get("widgets", []),
                layout=default_config.get("layout", "default"),
                refresh_interval=default_config.get("refresh_interval", 300)
            )

        return self._dashboard_store[user_id]

    def update_dashboard_config(self, user_id: int, **updates) -> DashboardConfig:
        """
        Update dashboard configuration.

        Args:
            user_id: User ID
            **updates: Fields to update

        Returns:
            Updated DashboardConfig
        """
        logger.info(f"Updating dashboard config for user {user_id}")

        config = self.get_dashboard_config(user_id)

        # Update fields
        for key, value in updates.items():
            if hasattr(config, key) and value is not None:
                setattr(config, key, value)

        self._dashboard_store[user_id] = config

        return config

