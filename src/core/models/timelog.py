from typing import Optional, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .project import Project


class TimeLog(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_fk: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.utcnow(), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    project: Mapped[list["Project"]] = relationship(
        secondary="timelog_project_association_table", back_populates="timelog")
    user: Mapped[list["User"]] = relationship(
        back_populates="timelog", uselist=True)