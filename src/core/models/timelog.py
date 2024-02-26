from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .base import Base

if TYPE_CHECKING:
    from .user import User


class TimeLog(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_fk: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped[list["User"]] = relationship(
        back_populates="timelog", uselist=True)
