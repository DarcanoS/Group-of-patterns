"""
Strategy Pattern - Concrete implementations of risk category strategies.
"""

from app.services.risk_category.interfaces import (
    RiskCategoryStrategy,
    RiskCategory,
    RiskLevel
)


class SimpleRiskCategoryStrategy(RiskCategoryStrategy):
    """
    STRATEGY PATTERN: Simple AQI risk categorization based on US EPA standards.

    This is a concrete strategy that uses basic AQI ranges.
    """

    def get_category(self, aqi: int) -> RiskCategory:
        """
        Categorize AQI using simple US EPA ranges.

        AQI ranges:
        - 0-50: Good
        - 51-100: Moderate
        - 101-150: Unhealthy for Sensitive Groups
        - 151-200: Unhealthy
        - 201-300: Very Unhealthy
        - 301+: Hazardous

        Args:
            aqi: Air Quality Index value

        Returns:
            RiskCategory object
        """
        if aqi <= 50:
            return RiskCategory(
                level=RiskLevel.GOOD,
                label="Good",
                color="#00e400",
                description="Air quality is satisfactory, and air pollution poses little or no risk."
            )
        elif aqi <= 100:
            return RiskCategory(
                level=RiskLevel.MODERATE,
                label="Moderate",
                color="#ffff00",
                description="Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
            )
        elif aqi <= 150:
            return RiskCategory(
                level=RiskLevel.UNHEALTHY_SENSITIVE,
                label="Unhealthy for Sensitive Groups",
                color="#ff7e00",
                description="Members of sensitive groups may experience health effects. The general public is less likely to be affected."
            )
        elif aqi <= 200:
            return RiskCategory(
                level=RiskLevel.UNHEALTHY,
                label="Unhealthy",
                color="#ff0000",
                description="Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
            )
        elif aqi <= 300:
            return RiskCategory(
                level=RiskLevel.VERY_UNHEALTHY,
                label="Very Unhealthy",
                color="#99004c",
                description="Health alert: The risk of health effects is increased for everyone."
            )
        else:
            return RiskCategory(
                level=RiskLevel.HAZARDOUS,
                label="Hazardous",
                color="#7e0023",
                description="Health warning of emergency conditions: everyone is more likely to be affected."
            )


class WhoRiskCategoryStrategy(RiskCategoryStrategy):
    """
    STRATEGY PATTERN: WHO-based AQI risk categorization.

    This concrete strategy uses WHO air quality guidelines which are more stringent.
    """

    def get_category(self, aqi: int) -> RiskCategory:
        """
        Categorize AQI using WHO guidelines (stricter thresholds).

        WHO typically has stricter standards than US EPA.

        Args:
            aqi: Air Quality Index value

        Returns:
            RiskCategory object
        """
        # WHO guidelines are stricter, so thresholds are lower
        if aqi <= 25:
            return RiskCategory(
                level=RiskLevel.GOOD,
                label="Good (WHO)",
                color="#00e400",
                description="Air quality meets WHO guidelines. Little to no health risk."
            )
        elif aqi <= 50:
            return RiskCategory(
                level=RiskLevel.MODERATE,
                label="Moderate (WHO)",
                color="#ffff00",
                description="Air quality is acceptable but may pose a risk for sensitive individuals."
            )
        elif aqi <= 100:
            return RiskCategory(
                level=RiskLevel.UNHEALTHY_SENSITIVE,
                label="Unhealthy for Sensitive (WHO)",
                color="#ff7e00",
                description="Sensitive groups should reduce prolonged outdoor exertion."
            )
        elif aqi <= 150:
            return RiskCategory(
                level=RiskLevel.UNHEALTHY,
                label="Unhealthy (WHO)",
                color="#ff0000",
                description="Everyone may begin to experience health effects. Sensitive groups should avoid outdoor activities."
            )
        elif aqi <= 250:
            return RiskCategory(
                level=RiskLevel.VERY_UNHEALTHY,
                label="Very Unhealthy (WHO)",
                color="#99004c",
                description="Health alert: everyone may experience more serious health effects."
            )
        else:
            return RiskCategory(
                level=RiskLevel.HAZARDOUS,
                label="Hazardous (WHO)",
                color="#7e0023",
                description="Emergency conditions: the entire population is likely to be affected."
            )

