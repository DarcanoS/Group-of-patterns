"""
Database session management.
Creates SQLAlchemy engine and session factory.
"""

from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from app.config import settings
from app.logging_config import get_logger

logger = get_logger(__name__)

# Create database engine
# Using NullPool for ingestion service (short-lived connections)
engine = create_engine(
    settings.database_url_computed,
    poolclass=NullPool,
    echo=False,  # Set to True for SQL query debugging
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    
    Yields:
        Database session
        
    Usage:
        db = next(get_db())
        try:
            # Use db
            ...
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    """
    Test database connectivity.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        db = next(get_db())
        # Simple query to test connection
        db.execute(text("SELECT 1"))
        logger.info("✓ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False
    finally:
        db.close()
