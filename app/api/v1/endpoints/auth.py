from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.api.v1.schemas.auth import UserRegister, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED, summary="Register a new user")
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Registers a new user account and returns an access token."""
    user = AuthService.register_user(db, user_in)
    access_token = create_access_token(subject=user.id)
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=Token, summary="Authenticate user")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticates a user via email and password."""
    return AuthService.authenticate_user(db, credentials)


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Returns the profile of the currently authenticated user."""
    return UserResponse.model_validate(current_user)
