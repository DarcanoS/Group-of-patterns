"""
AirQualityReading ORM model.
Represents individual air quality measurements from monitoring stations.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base


class AirQualityReading(Base):
    """
    AirQualityReading model - represents individual air quality measurements.

    Attributes:
        id: Primary key
        station_id: Foreign key to Station
        pollutant_id: Foreign key to Pollutant
        datetime: Timestamp of the reading
        value: Measured value of the pollutant
        aqi: Air Quality Index calculated for this reading

    Relationships:
        station: The monitoring station where reading was taken
        pollutant: The type of pollutant measured
    """

    __tablename__ = "air_quality_reading"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey("station.id"), nullable=False)
    pollutant_id = Column(Integer, ForeignKey("pollutant.id"), nullable=False)
    datetime = Column(TIMESTAMP(timezone=True), nullable=False)
    value = Column(Float, nullable=False)
    aqi = Column(Integer, nullable=True)

    # Relationships
    station = relationship("Station", backref="readings")
    pollutant = relationship("Pollutant", backref="readings")

    def __repr__(self):
        return f"<AirQualityReading(id={self.id}, station_id={self.station_id}, aqi={self.aqi})>"

