#!/usr/bin/env python3
"""Simple test to verify imports work."""

print("Testing imports...")

print("1. Importing app...")
from app.main import app
print("✓ app imported")

print("2. Importing design patterns...")
from app.services.risk_category import SimpleRiskCategoryStrategy
from app.services.recommendation_service import RecommendationFactory
from app.services.dashboard_service import DashboardResponseBuilder, default_dashboard_prototype
print("✓ Design patterns imported")

print("3. Testing Strategy Pattern...")
strategy = SimpleRiskCategoryStrategy()
result = strategy.get_category(75)
print(f"✓ Strategy: AQI 75 = {result.label}")

print("4. Testing Factory Pattern...")
recommendation = RecommendationFactory.create_for_aqi(120, "Citizen", "Bogotá")
print(f"✓ Factory: Created {recommendation.category} recommendation")

print("5. Testing Builder Pattern...")
builder = DashboardResponseBuilder()
dashboard = builder.with_overall_aqi(85).build()
print(f"✓ Builder: Created dashboard with AQI {dashboard.overall_aqi}")

print("6. Testing Prototype Pattern...")
config = default_dashboard_prototype.clone_for_user(1, "Bogotá", "dark")
print(f"✓ Prototype: Cloned config for user with {len(config['widgets'])} widgets")

print("\n✓✓✓ ALL BASIC TESTS PASSED! ✓✓✓")

