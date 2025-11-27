"""
Script to test database connections (PostgreSQL and MongoDB).
Run this to verify that the database configurations are correct.
"""

import asyncio
import sys
from sqlalchemy import text
from app.core.config import settings
from app.core.logging_config import logger
from app.db.session import engine
from app.db.mongodb import MongoDB


async def test_postgres_connection():
    """Test PostgreSQL connection."""
    try:
        logger.info("Testing PostgreSQL connection...")
        logger.info(f"Connection URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'N/A'}")

        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"✓ PostgreSQL connection successful!")
            logger.info(f"  Version: {version[:50]}...")

            # Test if PostGIS is available
            try:
                result = connection.execute(text("SELECT PostGIS_version()"))
                postgis_version = result.fetchone()[0]
                logger.info(f"  PostGIS version: {postgis_version}")
            except Exception as e:
                logger.warning(f"  PostGIS not available: {e}")

            return True
    except Exception as e:
        logger.error(f"✗ PostgreSQL connection failed: {e}")
        return False


async def test_mongodb_connection():
    """Test MongoDB connection."""
    try:
        if not settings.NOSQL_URI:
            logger.warning("MongoDB URI not configured, skipping test")
            return None

        logger.info("Testing MongoDB connection...")
        logger.info(f"Connection URI: {settings.NOSQL_URI.split('@')[1].split('?')[0] if '@' in settings.NOSQL_URI else 'N/A'}")

        await MongoDB.connect()

        # Test database operations
        db = MongoDB.get_database()

        # Get server info
        server_info = await db.client.server_info()
        logger.info(f"✓ MongoDB connection successful!")
        logger.info(f"  Version: {server_info.get('version', 'unknown')}")
        logger.info(f"  Database: {settings.NOSQL_DB_NAME}")

        # List collections
        collections = await db.list_collection_names()
        logger.info(f"  Collections: {len(collections)} found")
        if collections:
            logger.info(f"  Collection names: {', '.join(collections[:5])}")

        return True
    except Exception as e:
        logger.error(f"✗ MongoDB connection failed: {e}")
        return False
    finally:
        await MongoDB.disconnect()


async def main():
    """Run all connection tests."""
    logger.info("=" * 60)
    logger.info("DATABASE CONNECTION TESTS")
    logger.info("=" * 60)

    # Test PostgreSQL
    postgres_ok = await test_postgres_connection()
    print()

    # Test MongoDB
    mongodb_ok = await test_mongodb_connection()
    print()

    # Summary
    logger.info("=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"PostgreSQL: {'✓ OK' if postgres_ok else '✗ FAILED'}")
    if mongodb_ok is not None:
        logger.info(f"MongoDB:    {'✓ OK' if mongodb_ok else '✗ FAILED'}")
    else:
        logger.info(f"MongoDB:    ⊘ NOT CONFIGURED")
    logger.info("=" * 60)

    # Exit with appropriate code
    if not postgres_ok:
        sys.exit(1)
    elif mongodb_ok is False:  # Only fail if MongoDB is configured but connection failed
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())

