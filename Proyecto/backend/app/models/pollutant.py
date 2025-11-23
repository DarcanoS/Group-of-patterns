"""
Pollutant ORM model.
Represents air pollutants that are monitored (PM2.5, PM10, CO, etc.).
"""

from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base


class Pollutant(Base):
    """
    Pollutant model - represents types of air pollutants.

    Attributes:
        id: Primary key
        name: Pollutant name (e.g., 'PM2.5', 'CO', 'NO2')
        unit: Measurement unit (e.g., 'µg/m³', 'ppm')
        description: Detailed description of the pollutant
    """

    __tablename__ = "pollutant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Pollutant(id={self.id}, name='{self.name}', unit='{self.unit}')>"

