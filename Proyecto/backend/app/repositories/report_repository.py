"""
Report repository for database operations.
Handles CRUD operations for Report model.
"""

from typing import Optional, List
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.report import Report


class ReportRepository:
    """Repository for Report-related database operations."""

    def __init__(self, db: Session):
        """
        Initialize ReportRepository.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_by_id(self, report_id: int) -> Optional[Report]:
        """
        Get report by ID.

        Args:
            report_id: Report ID

        Returns:
            Report object or None
        """
        return self.db.query(Report).filter(Report.id == report_id).first()

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Report]:
        """
        Get reports for a user.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reports
        """
        return (
            self.db.query(Report)
            .filter(Report.user_id == user_id)
            .order_by(desc(Report.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, user_id: int, city: str, start_date: date, end_date: date,
               station_id: Optional[int] = None, pollutant_id: Optional[int] = None,
               file_path: Optional[str] = None) -> Report:
        """
        Create a new report.

        Args:
            user_id: User ID
            city: City for the report
            start_date: Report start date
            end_date: Report end date
            station_id: Optional station ID filter
            pollutant_id: Optional pollutant ID filter
            file_path: Optional path to generated report file

        Returns:
            Created report object
        """
        report = Report(
            user_id=user_id,
            created_at=datetime.utcnow(),
            city=city,
            start_date=start_date,
            end_date=end_date,
            station_id=station_id,
            pollutant_id=pollutant_id,
            file_path=file_path
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def update_file_path(self, report_id: int, file_path: str) -> Optional[Report]:
        """
        Update report file path.

        Args:
            report_id: Report ID
            file_path: New file path

        Returns:
            Updated report object or None
        """
        report = self.get_by_id(report_id)
        if not report:
            return None

        report.file_path = file_path
        self.db.commit()
        self.db.refresh(report)
        return report

    def delete(self, report_id: int) -> bool:
        """
        Delete a report.

        Args:
            report_id: Report ID

        Returns:
            True if deleted, False otherwise
        """
        report = self.get_by_id(report_id)
        if not report:
            return False

        self.db.delete(report)
        self.db.commit()
        return True

