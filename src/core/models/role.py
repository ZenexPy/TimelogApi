from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Role(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["User"] = relationship(back_populates="role", uselist=False)