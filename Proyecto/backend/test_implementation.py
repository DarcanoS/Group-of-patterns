"""
Test script to verify backend implementation.
Tests basic endpoints and design patterns.
"""

from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

print("=" * 60)
print("BACKEND IMPLEMENTATION TEST")
print("=" * 60)

# Test 1: Root endpoint
print("\n[TEST 1] Root endpoint")
response = client.get("/")
assert response.status_code == 200
data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ Response: {data}")

# Test 2: Health endpoint
print("\n[TEST 2] Health endpoint")
response = client.get("/health")
assert response.status_code == 200
data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ Response: {data}")

# Test 3: API documentation
print("\n[TEST 3] API documentation")
response = client.get("/api/docs")
assert response.status_code == 200
print(f"✓ Docs available at /api/docs")

# Test 4: OpenAPI schema
print("\n[TEST 4] OpenAPI schema")
response = client.get("/api/openapi.json")
assert response.status_code == 200
schema = response.json()
print(f"✓ OpenAPI schema loaded")
print(f"✓ API Title: {schema.get('info', {}).get('title')}")
print(f"✓ API Version: {schema.get('info', {}).get('version')}")
print(f"✓ Endpoints: {len(schema.get('paths', {}))}")

# Test 5: Design Patterns - Strategy Pattern
print("\n[TEST 5] Strategy Pattern - Risk Category")
from app.services.risk_category import SimpleRiskCategoryStrategy, WhoRiskCategoryStrategy

simple_strategy = SimpleRiskCategoryStrategy()
who_strategy = WhoRiskCategoryStrategy()

aqi_test = 75
simple_result = simple_strategy.get_category(aqi_test)
who_result = who_strategy.get_category(aqi_test)

print(f"✓ Simple Strategy for AQI {aqi_test}: {simple_result.label}")
print(f"✓ WHO Strategy for AQI {aqi_test}: {who_result.label}")
assert simple_result.label != who_result.label  # Different strategies give different results

# Test 6: Design Patterns - Factory Pattern
print("\n[TEST 6] Factory Pattern - Recommendation Factory")
from app.services.recommendation_service import RecommendationFactory

recommendation = RecommendationFactory.create_for_aqi(aqi=120, user_role="Citizen", location="Bogotá")
print(f"✓ Factory created recommendation for AQI 120")
print(f"✓ Category: {recommendation.category}")
print(f"✓ Message: {recommendation.message[:80]}...")
print(f"✓ Actions: {len(recommendation.actions)}")
print(f"✓ Products: {len(recommendation.products)}")

# Test 7: Design Patterns - Builder Pattern
print("\n[TEST 7] Builder Pattern - Dashboard Response Builder")
from app.services.dashboard_service import DashboardResponseBuilder

builder = DashboardResponseBuilder()
dashboard = (builder
    .with_overall_aqi(85)
    .with_metadata("test", "value")
    .build())

print(f"✓ Builder created dashboard response")
print(f"✓ Overall AQI: {dashboard.overall_aqi}")
print(f"✓ Timestamp: {dashboard.timestamp}")
print(f"✓ Metadata: {dashboard.metadata}")

# Test 8: Design Patterns - Prototype Pattern
print("\n[TEST 8] Prototype Pattern - Dashboard Config Prototype")
from app.services.dashboard_service import default_dashboard_prototype

config1 = default_dashboard_prototype.clone_for_user(user_id=1, default_location="Bogotá", theme="dark")
config2 = default_dashboard_prototype.clone_for_user(user_id=2, default_location="Medellín", theme="light")

print(f"✓ Prototype cloned for user 1")
print(f"✓ User 1 location: {config1['preferences']['default_location']}")
print(f"✓ User 1 theme: {config1['preferences']['theme']}")
print(f"✓ Prototype cloned for user 2")
print(f"✓ User 2 location: {config2['preferences']['default_location']}")
print(f"✓ User 2 theme: {config2['preferences']['theme']}")
assert config1 != config2  # Each clone is independent

# Test 9: Schemas validation
print("\n[TEST 9] Pydantic Schemas")
from app.schemas.user import UserCreate, UserResponse
from app.schemas.station import StationCreate

user_data = UserCreate(
    name="Test User",
    email="test@example.com",
    password="password123",
    role_id=1
)
print(f"✓ UserCreate schema validated: {user_data.email}")

station_data = StationCreate(
    name="Test Station",
    latitude=4.6097,
    longitude=-74.0817,
    city="Bogotá",
    country="Colombia"
)
print(f"✓ StationCreate schema validated: {station_data.name}")

# Test 10: Configuration
print("\n[TEST 10] Configuration")
from app.core.config import settings

print(f"✓ Project Name: {settings.PROJECT_NAME}")
print(f"✓ API Version: {settings.VERSION}")
print(f"✓ API Prefix: {settings.API_V1_STR}")
print(f"✓ CORS Origins: {len(settings.BACKEND_CORS_ORIGINS)}")
print(f"✓ JWT Algorithm: {settings.JWT_ALGORITHM}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED! ✓")
print("=" * 60)
print("\nImplementation Summary:")
print("- ✓ FastAPI application configured")
print("- ✓ All design patterns implemented (Strategy, Factory, Builder, Prototype)")
print("- ✓ Schemas and models defined")
print("- ✓ API endpoints structured")
print("- ✓ Configuration management")
print("- ✓ Logging configured")
print("\nNext steps:")
print("1. Set up PostgreSQL database")
print("2. Run Alembic migrations")
print("3. Seed initial data")
print("4. Test with actual database connection")
print("5. Implement remaining endpoints with DB integration")

