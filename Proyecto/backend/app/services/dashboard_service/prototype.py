"""
Prototype Pattern - Default dashboard configuration that can be cloned.
"""

import copy
from typing import Dict, Any, List


class DashboardConfigPrototype:
    """
    PROTOTYPE PATTERN: Provides a reusable prototype for default dashboard configurations.

    This allows creating customized dashboard configurations by cloning a base prototype
    and then modifying specific fields.
    """

    def __init__(self):
        """Initialize the default dashboard configuration."""
        self._config = {
            "layout": "default",
            "refresh_interval": 300,  # 5 minutes in seconds
            "widgets": [
                {
                    "id": "current-aqi",
                    "type": "aqi-display",
                    "position": {"row": 0, "col": 0, "width": 2, "height": 2},
                    "settings": {
                        "show_color": True,
                        "show_trend": True
                    }
                },
                {
                    "id": "pollutants-chart",
                    "type": "chart",
                    "position": {"row": 0, "col": 2, "width": 4, "height": 2},
                    "settings": {
                        "chart_type": "line",
                        "time_range": "24h",
                        "pollutants": ["PM2.5", "PM10", "O3"]
                    }
                },
                {
                    "id": "recommendations",
                    "type": "recommendations",
                    "position": {"row": 2, "col": 0, "width": 3, "height": 2},
                    "settings": {
                        "show_products": True,
                        "max_items": 5
                    }
                },
                {
                    "id": "map",
                    "type": "map",
                    "position": {"row": 2, "col": 3, "width": 3, "height": 2},
                    "settings": {
                        "zoom_level": 10,
                        "show_stations": True,
                        "show_heat_map": True
                    }
                },
                {
                    "id": "alerts",
                    "type": "alerts",
                    "position": {"row": 4, "col": 0, "width": 2, "height": 1},
                    "settings": {
                        "show_active_only": True
                    }
                }
            ],
            "preferences": {
                "default_location": None,
                "favorite_stations": [],
                "theme": "light"
            }
        }

    def clone(self) -> Dict[str, Any]:
        """
        Clone the prototype configuration.

        Returns a deep copy of the configuration that can be modified
        without affecting the original prototype.

        Returns:
            Deep copy of the dashboard configuration
        """
        return copy.deepcopy(self._config)

    def clone_for_user(self, user_id: int, default_location: str = None,
                      theme: str = "light") -> Dict[str, Any]:
        """
        Clone and customize the prototype for a specific user.

        Args:
            user_id: User ID
            default_location: User's default location
            theme: UI theme preference

        Returns:
            Customized dashboard configuration
        """
        config = self.clone()

        # Customize for user
        config["user_id"] = user_id
        config["preferences"]["default_location"] = default_location
        config["preferences"]["theme"] = theme

        return config

    def get_minimal_config(self) -> Dict[str, Any]:
        """
        Get a minimal dashboard configuration (fewer widgets).

        Useful for mobile or limited screen sizes.

        Returns:
            Minimal dashboard configuration
        """
        config = self.clone()

        # Keep only essential widgets
        config["widgets"] = [
            widget for widget in config["widgets"]
            if widget["type"] in ["aqi-display", "recommendations"]
        ]

        config["layout"] = "minimal"

        return config


# Global prototype instance
default_dashboard_prototype = DashboardConfigPrototype()

