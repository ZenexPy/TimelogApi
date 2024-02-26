from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


class Position(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    def __str__(self) -> str:
        return f"({self.id}) | {self.__class__.__name__.lower()} - ({self.title})"

    def __repr__(self) -> str:
        return str(self)