from typing import Annotated, Optional
from sqlalchemy import TIMESTAMP, MetaData, Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import Boolean, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship, DeclarativeBase, declared_attr, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Role(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


    user: Mapped["User"] = relationship(back_populates="role", uselist=False)


class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(75), nullable=False)
    second_name: Mapped[str] = mapped_column(String(75), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(nullable=False)

    role_fk: Mapped[int] = mapped_column(ForeignKey('role.id'))

    role: Mapped["Role"] = relationship(back_populates="user", uselist=False)
    timelog: Mapped[list["TimeLog"]] = relationship(
        back_populates="user", uselist=False)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}), (username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)


class Position(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    def __str__(self) -> str:
        return f"({self.id}) | {self.__class__.__name__.lower()} - ({self.title})"

    def __repr__(self) -> str:
        return str(self)


class TimeLog(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_fk: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped[list["User"]] = relationship(
        back_populates="timelog", uselist=True)


class Project(Base): #Many-to-Many
    pass

