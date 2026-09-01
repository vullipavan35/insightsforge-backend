from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.models.base import TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.dataset import Dataset


class Insight(Base, TimestampMixin):
    __tablename__ = "insights"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    insight_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(1000), nullable=False)
    score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    impact: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="insights")
