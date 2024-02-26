from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from datetime import datetime


class Project(Base):  # Many-to-Many
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    secret_name: Mapped[str] = mapped_column(String(40), nullable=False)