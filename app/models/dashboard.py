from typing import Optional
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from app.models.base import TimestampMixin, generate_uuid


class Dashboard(Base, TimestampMixin):
    __tablename__ = "dashboards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    layout: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
