from typing import Optional
from sqlalchemy import ForeignKey, DateTime, func, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .base import Base
from fastapi_users.db import SQLAlchemyBaseUserTable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .timelog import TimeLog
    from .position import Position


class User(SQLAlchemyBaseUserTable[int], Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(length=25), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.utcnow(), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)

    position_fk: Mapped[int] = mapped_column(ForeignKey('position.id'), nullable=False)

    timelog: Mapped[list["TimeLog"]] = relationship(
        back_populates="user", uselist=True)

    position: Mapped["Position"] = relationship(
        back_populates="user", uselist=False
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}), (username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)
