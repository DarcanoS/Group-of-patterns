"""
Factory Pattern - Recommendation factory for creating personalized recommendations.
"""

from app.services.recommendation_service.models import BaseRecommendation, ProductInfo


class RecommendationFactory:
    """
    FACTORY PATTERN: Creates appropriate recommendation objects based on AQI and context.

    This factory centralizes the logic for generating recommendations based on
    pollution levels and user roles.
    """

    @staticmethod
    def create_for_aqi(aqi: int, user_role: str = "Citizen", location: str = "") -> BaseRecommendation:
        """
        Create a recommendation based on AQI value and user role.

        Args:
            aqi: Air Quality Index value
            user_role: User's role (Citizen, Researcher, Admin)
            location: Location name for context

        Returns:
            BaseRecommendation object with tailored advice
        """
        # Determine recommendation category based on AQI
        if aqi <= 50:
            return RecommendationFactory._create_good_recommendation(aqi, user_role, location)
        elif aqi <= 100:
            return RecommendationFactory._create_moderate_recommendation(aqi, user_role, location)
        elif aqi <= 150:
            return RecommendationFactory._create_unhealthy_sensitive_recommendation(aqi, user_role, location)
        elif aqi <= 200:
            return RecommendationFactory._create_unhealthy_recommendation(aqi, user_role, location)
        elif aqi <= 300:
            return RecommendationFactory._create_very_unhealthy_recommendation(aqi, user_role, location)
        else:
            return RecommendationFactory._create_hazardous_recommendation(aqi, user_role, location)

    @staticmethod
    def _create_good_recommendation(aqi: int, user_role: str, location: str) -> BaseRecommendation:
        """Create recommendation for good air quality (AQI 0-50)."""
        message = f"Air quality in {location} is good (AQI: {aqi}). It's a great day for outdoor activities!"

        if user_role == "Researcher":
            message += " Data shows optimal conditions for monitoring baseline pollutant levels."

        return BaseRecommendation(
            pollution_level=aqi,
            message=message,
            category="good",
            products=[],
            actions=[
                "Enjoy outdoor activities",
                "Perfect time for exercise",
                "Open windows to ventilate your home"
            ]
        )

    @staticmethod
    def _create_moderate_recommendation(aqi: int, user_role: str, location: str) -> BaseRecommendation:
        """Create recommendation for moderate air quality (AQI 51-100)."""
        message = f"Air quality in {location} is moderate (AQI: {aqi}). Air quality is acceptable for most people."

        if user_role == "Researcher":
            message += " Consider monitoring sensitive population responses."

        return BaseRecommendation(
            pollution_level=aqi,
            message=message,
            category="moderate",
            products=[],
            actions=[
                "Most people can enjoy outdoor activities",
                "Unusually sensitive people should consider reducing prolonged outdoor exertion",
                "Monitor air quality if you have respiratory conditions"
            ]
        )

    @staticmethod
    def _create_unhealthy_sensitive_recommendation(aqi: int, user_role: str, location: str) -> BaseRecommendation:
        """Create recommendation for unhealthy for sensitive groups (AQI 101-150)."""
        message = f"Air quality in {location} is unhealthy for sensitive groups (AQI: {aqi}). Take precautions if you are sensitive to air pollution."

        products = [
            ProductInfo(name="Basic Face Mask", type="mask", url="https://example.com/mask"),
            ProductInfo(name="Air Quality Monitor", type="monitor", url="https://example.com/monitor")
        ]

        if user_role == "Researcher":
            message += " Elevated levels detected - recommend sampling for analysis."

        return BaseRecommendation(
            pollution_level=aqi,
            message=message,
            category="unhealthy_for_sensitive",
            products=products,
            actions=[
                "Sensitive groups should reduce prolonged outdoor exertion",
                "Consider wearing a mask outdoors",
                "Keep windows closed",
                "Use air purifiers indoors"
            ]
        )

    @staticmethod
    def _create_unhealthy_recommendation(aqi: int, user_role: str, location: str) -> BaseRecommendation:
        """Create recommendation for unhealthy air quality (AQI 151-200)."""
        message = f"Air quality in {location} is unhealthy (AQI: {aqi}). Everyone may experience health effects."

        products = [
            ProductInfo(name="N95 Respirator Mask", type="respirator", url="https://example.com/n95"),
            ProductInfo(name="HEPA Air Purifier", type="air_purifier", url="https://example.com/purifier"),
            ProductInfo(name="Indoor Air Quality Monitor", type="monitor", url="https://example.com/monitor")
        ]

        if user_role == "Researcher":
            message += " Critical pollution event - immediate analysis recommended."

        return BaseRecommendation(
            pollution_level=aqi,
            message=message,
            category="unhealthy",
            products=products,
            actions=[
                "Avoid prolonged outdoor activities",
                "Wear N95 mask if you must go outside",
                "Keep windows and doors closed",
                "Run air purifiers on high",
                "Sensitive groups should stay indoors"
            ]
        )

    @staticmethod
    def _create_very_unhealthy_recommendation(aqi: int, user_role: str, location: str) -> BaseRecommendation:
        """Create recommendation for very unhealthy air quality (AQI 201-300)."""
        message = f"Air quality in {location} is very unhealthy (AQI: {aqi}). Health alert - everyone may experience serious health effects."

        products = [
            ProductInfo(name="N95/N99 Respirator", type="respirator", url="https://example.com/n95"),
            ProductInfo(name="Professional HEPA Air Purifier", type="air_purifier", url="https://example.com/pro-purifier"),
            ProductInfo(name="Emergency Air Quality Kit", type="kit", url="https://example.com/kit")
        ]

        if user_role == "Admin":
            message += " ALERT: Issue public health advisory immediately."

        return BaseRecommendation(
            pollution_level=aqi,
            message=message,
            category="very_unhealthy",
            products=products,
            actions=[
                "Stay indoors as much as possible",
                "Avoid all outdoor physical activity",
                "Wear high-grade respirator if you must go outside",
                "Seal windows and doors",
                "Use multiple air purifiers",
                "Check on vulnerable neighbors"
            ]
        )

    @staticmethod
    def _create_hazardous_recommendation(aqi: int, user_role: str, location: str) -> BaseRecommendation:
        """Create recommendation for hazardous air quality (AQI 301+)."""
        message = f"HAZARDOUS air quality in {location} (AQI: {aqi}). Health emergency - everyone is likely to be affected."

        products = [
            ProductInfo(name="Professional Respirator (P100)", type="respirator", url="https://example.com/p100"),
            ProductInfo(name="Hospital-Grade Air Purifier", type="air_purifier", url="https://example.com/hospital-purifier"),
            ProductInfo(name="Emergency Evacuation Kit", type="kit", url="https://example.com/evac-kit")
        ]

        if user_role == "Admin":
            message += " EMERGENCY: Activate emergency response protocols."

        return BaseRecommendation(
            pollution_level=aqi,
            message=message,
            category="hazardous",
            products=products,
            actions=[
                "EMERGENCY: Stay indoors at all times",
                "Do NOT go outside unless absolutely necessary",
                "Wear P100 respirator if evacuation required",
                "Seal all windows, doors, and vents",
                "Run air purifiers continuously",
                "Consider evacuation if possible",
                "Monitor health symptoms closely",
                "Keep emergency contacts ready"
            ]
        )

