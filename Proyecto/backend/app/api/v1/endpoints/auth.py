"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.auth_service import AuthService
from app.schemas.auth import LoginResponse
from app.schemas.user import UserResponse
from app.models.user import AppUser
from app.core.logging_config import logger

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login.

    Get an access token for future requests.
    """
    auth_service = AuthService(db)

    result = auth_service.login(
        email=form_data.username,  # OAuth2 uses 'username' field
        password=form_data.password
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"User logged in: {result['user'].email}")

    return LoginResponse(
        access_token=result["access_token"],
        token_type=result["token_type"],
        user=UserResponse.model_validate(result["user"])
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: AppUser = Depends(get_current_user)
):
    """
    Get current user information.

    Returns the currently authenticated user's profile.
    """
    return UserResponse.model_validate(current_user)

