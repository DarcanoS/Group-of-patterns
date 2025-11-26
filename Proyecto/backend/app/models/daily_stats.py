"""
AirQualityDailyStats ORM model.
Represents aggregated daily statistics for air quality data.
"""

from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class AirQualityDailyStats(Base):
    """
    AirQualityDailyStats model - represents daily aggregated air quality statistics.

    Attributes:
        id: Primary key
        station_id: Foreign key to Station
        pollutant_id: Foreign key to Pollutant
        date: Date for which statistics are calculated
        avg_value: Average pollutant value for the day
        avg_aqi: Average AQI for the day
        max_aqi: Maximum AQI recorded during the day
        min_aqi: Minimum AQI recorded during the day
        readings_count: Number of readings used to calculate statistics

    Relationships:
        station: The monitoring station
        pollutant: The pollutant measured
    """

    __tablename__ = "air_quality_daily_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("station.id"), nullable=False)
    pollutant_id = Column(Integer, ForeignKey("pollutant.id"), nullable=False)
    date = Column(Date, nullable=False)
    avg_value = Column(Float, nullable=True)
    avg_aqi = Column(Integer, nullable=True)
    max_aqi = Column(Integer, nullable=True)
    min_aqi = Column(Integer, nullable=True)
    readings_count = Column(Integer, nullable=False, default=0)

    # Relationships
    station = relationship("Station", backref="daily_stats")
    pollutant = relationship("Pollutant", backref="daily_stats")

    def __repr__(self):
        return f"<AirQualityDailyStats(id={self.id}, station_id={self.station_id}, date={self.date})>"

