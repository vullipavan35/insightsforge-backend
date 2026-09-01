from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func


class Base(DeclarativeBase):
    """Base model providing automatic table naming and timestamps."""
    pass
