"""
Reports endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportCreate, ReportResponse
from app.models.user import AppUser
from app.core.logging_config import logger

router = APIRouter()


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report_data: ReportCreate,
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new report.

    Creates a report metadata record. In production, this would also
    trigger report generation (PDF, CSV, etc.) and store the file.
    """
    report_repo = ReportRepository(db)

    # Create report with placeholder file path
    file_path = f"/reports/user_{current_user.id}/report_{report_data.city}_{report_data.start_date}_{report_data.end_date}.pdf"

    report = report_repo.create(
        user_id=current_user.id,
        city=report_data.city,
        start_date=report_data.start_date,
        end_date=report_data.end_date,
        station_id=report_data.station_id,
        pollutant_id=report_data.pollutant_id,
        file_path=file_path
    )

    logger.info(f"Report created by user {current_user.id}: {report.id}")

    return ReportResponse.model_validate(report)


@router.get("", response_model=List[ReportResponse])
def list_user_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List reports for the current user.

    Returns a paginated list of reports created by the user.
    """
    report_repo = ReportRepository(db)

    reports = report_repo.get_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

    return [ReportResponse.model_validate(r) for r in reports]


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific report by ID.

    Users can only access their own reports unless they are admin.
    """
    report_repo = ReportRepository(db)

    report = report_repo.get_by_id(report_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with id {report_id} not found"
        )

    # Check ownership (unless admin)
    if report.user_id != current_user.id and current_user.role.name != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this report"
        )

    return ReportResponse.model_validate(report)

