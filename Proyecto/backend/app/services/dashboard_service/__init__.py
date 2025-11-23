"""
Dashboard service initialization.
"""

from app.services.dashboard_service.builder import DashboardResponseBuilder, DashboardResponseSchema
from app.services.dashboard_service.prototype import DashboardConfigPrototype, default_dashboard_prototype

__all__ = [
    "DashboardResponseBuilder",
    "DashboardResponseSchema",
    "DashboardConfigPrototype",
    "default_dashboard_prototype",
]

