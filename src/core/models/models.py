from sqlalchemy import TIMESTAMP, MetaData, Table, Column, Integer, String, JSON, ForeignKey
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
    permissions: Mapped[str] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="role", uselist=False)


class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    registered_at: Mapped[TIMESTAMP] = Column(
        TIMESTAMP, default=datetime.utcnow)

    role_fk: Mapped[int] = mapped_column(ForeignKey('role.id'))
    role: Mapped["Role"] = relationship(back_populates="user", uselist=False)


class Product(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
