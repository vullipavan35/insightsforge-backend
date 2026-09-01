from typing import List, Optional
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.models.base import TimestampMixin, generate_uuid


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="member", nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="PRO", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    datasets: Mapped[List["Dataset"]] = relationship("Dataset", back_populates="owner", cascade="all, delete-orphan")
    subscription: Mapped[Optional["Subscription"]] = relationship("Subscription", back_populates="user", uselist=False)
