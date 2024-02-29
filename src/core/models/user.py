from typing import Optional
from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .base import Base


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .role import Role
    from .timelog import TimeLog


class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(75), nullable=False)
    second_name: Mapped[str] = mapped_column(String(75), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.utcnow(), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)

    role_fk: Mapped[int] = mapped_column(ForeignKey('role.id'))

    role: Mapped["Role"] = relationship(back_populates="user", uselist=False)
    timelog: Mapped[list["TimeLog"]] = relationship(
        back_populates="user", uselist=False)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}), (username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)
