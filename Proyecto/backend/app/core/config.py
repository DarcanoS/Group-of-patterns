"""
Application configuration using Pydantic settings.
Loads configuration from environment variables.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All configuration should be defined here and loaded from .env file.
    """

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Air Quality Platform API"
    VERSION: str = "1.0.0"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",")]
        return v

    # Database (PostgreSQL + PostGIS)
    DATABASE_URL: str

    # JWT Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # NoSQL (Future - MongoDB/Redis for settings)
    NOSQL_URI: str = ""
    NOSQL_DB_NAME: str = "airquality_nosql"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Application Settings
    FIRST_SUPERUSER_EMAIL: str = "admin@airquality.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


# Create a singleton instance of settings
settings = Settings()

