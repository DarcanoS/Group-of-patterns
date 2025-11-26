"""
MapRegion ORM model.
Represents geographical regions with optional PostGIS geometry.
"""

from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.db.base import Base


class MapRegion(Base):
    """
    MapRegion model - represents geographical regions.

    Attributes:
        id: Primary key
        name: Region name (e.g., 'Bogotá D.C.', 'Antioquia')
        geom: PostGIS geometry field for spatial queries (optional)
    """

    __tablename__ = "map_region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)

    def __repr__(self):
        return f"<MapRegion(id={self.id}, name='{self.name}')>"

