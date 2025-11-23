"""
Strategy Pattern - Interfaces and base classes for risk category strategies.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict


class RiskLevel(str, Enum):
    """Risk level categories."""
    GOOD = "good"
    MODERATE = "moderate"
    UNHEALTHY_SENSITIVE = "unhealthy_for_sensitive"
    UNHEALTHY = "unhealthy"
    VERY_UNHEALTHY = "very_unhealthy"
    HAZARDOUS = "hazardous"


class RiskCategory:
    """
    Risk category model with display information.

    Attributes:
        level: Risk level enum
        label: Human-readable label
        color: Color hint for UI (hex color code)
        description: Description of health implications
    """

    def __init__(self, level: RiskLevel, label: str, color: str, description: str):
        """
        Initialize RiskCategory.

        Args:
            level: Risk level
            label: Display label
            color: Hex color code
            description: Health description
        """
        self.level = level
        self.label = label
        self.color = color
        self.description = description

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "level": self.level.value,
            "label": self.label,
            "color": self.color,
            "description": self.description
        }


class RiskCategoryStrategy(ABC):
    """
    STRATEGY PATTERN: Abstract base class for AQI risk categorization strategies.

    This allows different algorithms to classify AQI values into risk categories.
    """

    @abstractmethod
    def get_category(self, aqi: int) -> RiskCategory:
        """
        Get risk category for an AQI value.

        Args:
            aqi: Air Quality Index value

        Returns:
            RiskCategory object
        """
        pass

