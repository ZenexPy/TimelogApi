from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

if TYPE_CHECKING:
    from .timelog import TimeLog



class Project(Base):  
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.utcnow(), nullable=False)
    secret_name: Mapped[str] = mapped_column(String(40), nullable=False)

    timelog: Mapped[list["TimeLog"]] = relationship(back_populates="project", uselist=True)
