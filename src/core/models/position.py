from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, func, String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

if TYPE_CHECKING:
    from .user import User


class Position(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    salary: Mapped[int] = mapped_column(default=0)

    user: Mapped[list["User"]] = relationship(back_populates="position", uselist=True)

    def __str__(self) -> str:
        return f"({self.id}) | {self.__class__.__name__.lower()} - ({self.title})"

    def __repr__(self) -> str:
        return str(self)
