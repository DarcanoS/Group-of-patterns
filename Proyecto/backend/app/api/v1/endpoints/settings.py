"""
Settings endpoints.
Uses Prototype pattern for dashboard configurations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.settings_service import SettingsService
from app.schemas.settings import UserPreferences, DashboardConfig, SettingsUpdateRequest
from app.models.user import AppUser

router = APIRouter()


@router.get("/preferences", response_model=UserPreferences)
def get_user_preferences(
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user preferences.

    Returns user-specific preferences like theme, language, notifications, etc.
    (Mock implementation - would use NoSQL in production)
    """
    settings_service = SettingsService(db)

    preferences = settings_service.get_user_preferences(current_user.id)

    return preferences


@router.put("/preferences", response_model=UserPreferences)
def update_user_preferences(
    settings_update: SettingsUpdateRequest,
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user preferences.

    Updates user-specific preferences.
    """
    settings_service = SettingsService(db)

    # Convert to dict and filter out None values
    updates = settings_update.model_dump(exclude_unset=True)

    preferences = settings_service.update_user_preferences(current_user.id, **updates)

    return preferences


@router.get("/dashboard", response_model=DashboardConfig)
def get_dashboard_config(
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard configuration for the current user.

    Uses Prototype pattern to clone default dashboard configuration
    for new users, then returns their personalized configuration.
    """
    settings_service = SettingsService(db)

    config = settings_service.get_dashboard_config(current_user.id)

    return config


@router.put("/dashboard", response_model=DashboardConfig)
def update_dashboard_config(
    dashboard_update: DashboardConfig,
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update dashboard configuration.

    Updates the user's dashboard layout, widgets, and settings.
    """
    settings_service = SettingsService(db)

    # Update with the full dashboard config
    config = settings_service.update_dashboard_config(
        current_user.id,
        widgets=dashboard_update.widgets,
        layout=dashboard_update.layout,
        refresh_interval=dashboard_update.refresh_interval
    )

    return config

