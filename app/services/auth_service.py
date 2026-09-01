from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User
from app.models.subscription import Subscription
from app.api.v1.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.utils.security import verify_password, get_password_hash, create_access_token


class AuthService:
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        return db.scalars(stmt).first()

    @staticmethod
    def register_user(db: Session, user_in: UserRegister) -> User:
        existing_user = AuthService.get_by_email(db, user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        new_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            role="member",
            plan="PRO",
            is_active=True,
        )
        db.add(new_user)
        db.flush()

        # Create default subscription
        sub = Subscription(
            user_id=new_user.id,
            plan="PRO",
            status="active",
            rows_processed=0,
            rows_limit=5000000,
            ai_queries_used=0,
            ai_queries_limit=5000,
        )
        db.add(sub)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, credentials: UserLogin) -> Token:
        email = credentials.email or credentials.username
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username is required.",
            )

        user = AuthService.get_by_email(db, email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account.",
            )

        access_token = create_access_token(subject=user.id)
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )
