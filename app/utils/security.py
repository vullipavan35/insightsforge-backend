from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Union
from jose import jwt, JWTError
import bcrypt
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Creates a signed JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """Decodes a JWT access token and returns the subject (user_id)."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        return user_id
    except JWTError:
        return None
