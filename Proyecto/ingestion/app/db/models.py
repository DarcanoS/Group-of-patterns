"""
Minimal SQLAlchemy ORM models for the ingestion service.
These models match the database schema defined in init_schema.sql
"""

from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

Base = declarative_base()


class MapRegion(Base):
    """Geographical regions with polygon boundaries"""
    __tablename__ = "map_region"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))


class Pollutant(Base):
    """Catalog of air pollutants"""
    __tablename__ = "pollutant"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    unit = Column(String(50), nullable=False)
    description = Column(Text)


class Station(Base):
    """Air quality monitoring stations"""
    __tablename__ = "station"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    region_id = Column(Integer, ForeignKey("map_region.id", ondelete="SET NULL"))
    
    # Relationships
    region = relationship("MapRegion", backref="stations")


class AirQualityReading(Base):
    """Individual sensor readings from stations"""
    __tablename__ = "air_quality_reading"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("station.id", ondelete="CASCADE"), nullable=False)
    pollutant_id = Column(Integer, ForeignKey("pollutant.id", ondelete="RESTRICT"), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False)
    value = Column(Float, nullable=False)
    aqi = Column(Integer)
    
    # Relationships
    station = relationship("Station", backref="readings")
    pollutant = relationship("Pollutant", backref="readings")


class AirQualityDailyStats(Base):
    """Aggregated daily statistics for analytics"""
    __tablename__ = "air_quality_daily_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("station.id", ondelete="CASCADE"), nullable=False)
    pollutant_id = Column(Integer, ForeignKey("pollutant.id", ondelete="RESTRICT"), nullable=False)
    date = Column(Date, nullable=False)
    avg_value = Column(Float)
    avg_aqi = Column(Integer)
    max_aqi = Column(Integer)
    min_aqi = Column(Integer)
    readings_count = Column(Integer, default=0)
    
    # Relationships
    station = relationship("Station")
    pollutant = relationship("Pollutant")
