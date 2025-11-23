"""
Station ORM model.
Represents air quality monitoring stations.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Station(Base):
    """
    Station model - represents air quality monitoring stations.

    Attributes:
        id: Primary key
        name: Station name
        latitude: Geographical latitude
        longitude: Geographical longitude
        city: City where station is located
        country: Country where station is located
        region_id: Foreign key to MapRegion

    Relationships:
        region: MapRegion this station belongs to
        readings: Air quality readings from this station
    """

    __tablename__ = "station"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    region_id = Column(Integer, ForeignKey("map_region.id"), nullable=True)

    # Relationships
    region = relationship("MapRegion", backref="stations")

    def __repr__(self):
        return f"<Station(id={self.id}, name='{self.name}', city='{self.city}')>"

