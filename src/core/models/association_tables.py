from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


# timelog_project_assosiation_table = Table(
#     "timelog_project",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("timelog_id", ForeignKey("timelog.id"), nullable=False),
#     Column("project_id", ForeignKey("project.id"), nullable=False),
#     UniqueConstraint("timelog_id", "project_id",
#                      name="idx_unique_timelog_project"),
# )


class TimelogProjectAssociation(Base):
    __tablename__ = "timelog_project_association_table"
    __table_args__ = (
        UniqueConstraint("timelog_id", "project_id",
                         name="idx_unique_timelog_project"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    timelog_id: Mapped[int] = mapped_column(ForeignKey("timelog.id"))
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"))
