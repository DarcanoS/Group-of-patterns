"""
MongoDB connection configuration.
Handles connection to MongoDB for application settings and configuration.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
from app.core.config import settings
from app.core.logging_config import logger


class MongoDB:
    """MongoDB connection manager."""

    client: Optional[AsyncIOMotorClient] = None
    sync_client: Optional[MongoClient] = None

    @classmethod
    async def connect(cls) -> None:
        """
        Create database connection.
        """
        try:
            if settings.NOSQL_URI:
                logger.info("Connecting to MongoDB...")
                cls.client = AsyncIOMotorClient(settings.NOSQL_URI)
                cls.sync_client = MongoClient(settings.NOSQL_URI)

                # Test the connection
                await cls.client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
            else:
                logger.warning("NOSQL_URI not configured, MongoDB connection skipped")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def disconnect(cls) -> None:
        """
        Close database connection.
        """
        try:
            if cls.client:
                cls.client.close()
                logger.info("Disconnected from MongoDB")
            if cls.sync_client:
                cls.sync_client.close()
        except Exception as e:
            logger.error(f"Error disconnecting from MongoDB: {e}")

    @classmethod
    def get_database(cls):
        """
        Get async database instance.

        Returns:
            AsyncIOMotorDatabase instance
        """
        if not cls.client:
            raise RuntimeError("MongoDB client not initialized. Call connect() first.")
        return cls.client[settings.NOSQL_DB_NAME]

    @classmethod
    def get_sync_database(cls):
        """
        Get sync database instance for non-async operations.

        Returns:
            Database instance
        """
        if not cls.sync_client:
            raise RuntimeError("MongoDB sync client not initialized. Call connect() first.")
        return cls.sync_client[settings.NOSQL_DB_NAME]


# Convenience functions
async def get_mongodb():
    """
    Dependency to get MongoDB database.

    Returns:
        AsyncIOMotorDatabase instance
    """
    return MongoDB.get_database()


async def get_mongodb_collection(collection_name: str):
    """
    Get a specific MongoDB collection.

    Args:
        collection_name: Name of the collection

    Returns:
        AsyncIOMotorCollection instance
    """
    db = MongoDB.get_database()
    return db[collection_name]

