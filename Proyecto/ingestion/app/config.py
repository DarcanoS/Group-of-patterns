"""
Configuration management for the ingestion service.
Loads settings from environment variables using Pydantic.
"""

import os
from pathlib import Path
from typing import Optional, List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Reads from .env file if present, with environment variables taking precedence.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ========================================================================
    # Database Configuration
    # ========================================================================
    
    database_url: str = Field(
        default="postgresql://air_quality_app:changeme@localhost:5432/air_quality_db",
        description="PostgreSQL connection URL"
    )
    
    db_host: Optional[str] = Field(default=None, description="Database host")
    db_port: Optional[int] = Field(default=None, description="Database port")
    db_name: Optional[str] = Field(default=None, description="Database name")
    db_user: Optional[str] = Field(default=None, description="Database user")
    db_password: Optional[str] = Field(default=None, description="Database password")
    
    # ========================================================================
    # External API Providers
    # ========================================================================
    
    # AQICN API Configuration
    aqicn_api_key: Optional[str] = Field(
        default=None,
        alias="TOKEN_API_AQICN",
        description="AQICN API token (get from https://aqicn.org/data-platform/token/)"
    )
    
    aqicn_base_url: str = Field(
        default="https://api.waqi.info",
        description="AQICN API base URL"
    )
    
    aqicn_cities: Optional[str] = Field(
        default="bogota",
        alias="AQICN_CITIES",
        description="Comma-separated list of cities to query (e.g., 'bogota,medellin,cali')"
    )
    
    # ========================================================================
    # Ingestion Behavior
    # ========================================================================
    
    historical_data_path: Path = Field(
        default=Path("../data_air"),
        description="Path to historical CSV and GeoJSON data files"
    )
    
    station_mapping_path: Path = Field(
        default=Path("data/station_mapping.yaml"),
        description="Path to station mapping configuration file"
    )
    
    ingestion_interval_minutes: int = Field(
        default=10,
        description="Interval in minutes between real-time API ingestion runs"
    )
    
    ingestion_default_cities: List[str] = Field(
        default=["Bogotá"],
        description="Default cities to ingest from AQICN API"
    )
    
    ingestion_time_window_minutes: int = Field(
        default=60,
        description="Time window in minutes for fetching recent data"
    )
    
    # ========================================================================
    # Logging
    # ========================================================================
    
    ingestion_log_level: str = Field(
        default="INFO",
        description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    
    log_format: str = Field(
        default="colorlog",
        description="Log format (colorlog or standard)"
    )
    
    # ========================================================================
    # Operational Modes
    # ========================================================================
    
    ingestion_mode: str = Field(
        default="historical",
        description="Ingestion mode: historical, realtime, or both"
    )
    
    allow_reingestion: bool = Field(
        default=True,
        description="Allow re-running historical ingestion (will skip duplicates)"
    )
    
    # ========================================================================
    # Computed Properties
    # ========================================================================
    
    @property
    def database_url_computed(self) -> str:
        """
        Compute database URL from individual components if not provided directly.
        """
        if self.database_url and not self.database_url.startswith("postgresql://air_quality_app:changeme"):
            return self.database_url
        
        if all([self.db_host, self.db_port, self.db_name, self.db_user, self.db_password]):
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        
        return self.database_url
    
    def get_historical_data_path(self) -> Path:
        """Get absolute path to historical data directory."""
        if self.historical_data_path.is_absolute():
            return self.historical_data_path
        
        # Resolve relative to ingestion service root
        base_path = Path(__file__).parent.parent
        return (base_path / self.historical_data_path).resolve()
    
    def get_station_mapping_path(self) -> Path:
        """Get absolute path to station mapping file."""
        if self.station_mapping_path.is_absolute():
            return self.station_mapping_path
        
        base_path = Path(__file__).parent.parent
        return (base_path / self.station_mapping_path).resolve()


# Global settings instance
settings = Settings()
