from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.models.base import TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.user import User


class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="PRO", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rows_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rows_limit: Mapped[int] = mapped_column(Integer, default=5000000, nullable=False)
    ai_queries_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ai_queries_limit: Mapped[int] = mapped_column(Integer, default=5000, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="subscription")
