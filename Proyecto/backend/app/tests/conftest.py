"""
Pytest configuration and fixtures.
"""

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Test database URL (use a separate test database)
TEST_DATABASE_URL = "postgresql://postgres:password@localhost:5432/airquality_test_db"

# Create test engine
test_engine = create_engine(TEST_DATABASE_URL)

# Create test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_engine():
    """
    Create test database engine.
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    # Drop all tables after tests
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """
    Create a new database session for each test.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with overridden database dependency.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """
    Sample user data for testing.
    """
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "location": "Test City"
    }

