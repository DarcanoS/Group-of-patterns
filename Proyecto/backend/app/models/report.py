"""
Report ORM model.
Represents user-generated air quality reports.
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base


class Report(Base):
    """
    Report model - represents generated air quality reports.

    Attributes:
        id: Primary key
        user_id: Foreign key to AppUser who created the report
        created_at: Timestamp when report was created
        city: City covered by the report
        start_date: Start date of the reporting period
        end_date: End date of the reporting period
        station_id: Optional foreign key to specific Station
        pollutant_id: Optional foreign key to specific Pollutant
        file_path: Path or URL to the generated report file

    Relationships:
        user: The user who created this report
        station: Optional specific station for the report
        pollutant: Optional specific pollutant for the report
    """

    __tablename__ = "report"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("app_user.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    city = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    station_id = Column(Integer, ForeignKey("station.id"), nullable=True)
    pollutant_id = Column(Integer, ForeignKey("pollutant.id"), nullable=True)
    file_path = Column(String(500), nullable=True)

    # Relationships
    user = relationship("AppUser", back_populates="reports")
    station = relationship("Station", backref="reports")
    pollutant = relationship("Pollutant", backref="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, user_id={self.user_id}, city='{self.city}')>"

