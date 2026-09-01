from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.models.base import TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.insight import Insight
    from app.models.forecast import Forecast


class Dataset(Base, TimestampMixin):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_format: Mapped[str] = mapped_column(String(20), default="csv", nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    col_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="READY", nullable=False, index=True)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quality_report: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="datasets")
    insights: Mapped[List["Insight"]] = relationship("Insight", back_populates="dataset", cascade="all, delete-orphan")
    forecasts: Mapped[List["Forecast"]] = relationship("Forecast", back_populates="dataset", cascade="all, delete-orphan")
