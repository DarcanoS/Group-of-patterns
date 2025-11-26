"""
Station repository for database operations.
Handles CRUD operations for Station model.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.station import Station


class StationRepository:
    """Repository for Station-related database operations."""

    def __init__(self, db: Session):
        """
        Initialize StationRepository.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, station_id: int) -> Optional[Station]:
        """
        Get station by ID.

        Args:
            station_id: Station ID

        Returns:
            Station object or None
        """
        return self.db.query(Station).filter(Station.id == station_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, city: Optional[str] = None,
                country: Optional[str] = None, region_id: Optional[int] = None) -> List[Station]:
        """
        Get all stations with optional filters.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            city: Filter by city
            country: Filter by country
            region_id: Filter by region ID

        Returns:
            List of stations
        """
        query = self.db.query(Station)

        if city:
            query = query.filter(Station.city.ilike(f"%{city}%"))
        if country:
            query = query.filter(Station.country.ilike(f"%{country}%"))
        if region_id:
            query = query.filter(Station.region_id == region_id)

        return query.offset(skip).limit(limit).all()

    def get_by_city(self, city: str) -> List[Station]:
        """
        Get stations by city.

        Args:
            city: City name

        Returns:
            List of stations in the city
        """
        return self.db.query(Station).filter(Station.city.ilike(f"%{city}%")).all()

    def create(self, name: str, latitude: float, longitude: float, city: str,
               country: str, region_id: Optional[int] = None) -> Station:
        """
        Create a new station.

        Args:
            name: Station name
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            city: City name
            country: Country name
            region_id: Region ID (optional)

        Returns:
            Created station object
        """
        station = Station(
            name=name,
            latitude=latitude,
            longitude=longitude,
            city=city,
            country=country,
            region_id=region_id
        )
        self.db.add(station)
        self.db.commit()
        self.db.refresh(station)
        return station

    def update(self, station_id: int, **kwargs) -> Optional[Station]:
        """
        Update station information.

        Args:
            station_id: Station ID
            **kwargs: Fields to update

        Returns:
            Updated station object or None
        """
        station = self.get_by_id(station_id)
        if not station:
            return None

        for key, value in kwargs.items():
            if hasattr(station, key) and value is not None:
                setattr(station, key, value)

        self.db.commit()
        self.db.refresh(station)
        return station

    def delete(self, station_id: int) -> bool:
        """
        Delete a station.

        Args:
            station_id: Station ID

        Returns:
            True if deleted, False otherwise
        """
        station = self.get_by_id(station_id)
        if not station:
            return False

        self.db.delete(station)
        self.db.commit()
        return True

