from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.models.base import TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.dataset import Dataset


class Forecast(Base, TimestampMixin):
    __tablename__ = "forecasts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    target_column: Mapped[str] = mapped_column(String(100), nullable=False)
    horizon_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    model_used: Mapped[str] = mapped_column(String(50), default="prophet", nullable=False)
    confidence_level: Mapped[float] = mapped_column(Float, default=0.95, nullable=False)
    results: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="forecasts")
