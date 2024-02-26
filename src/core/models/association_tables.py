from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from .base import Base


timelog_project_assosiation_table = Table(
    "timelog_project",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("timelog_id", ForeignKey("timelog.id"), nullable=False),
    Column("project_id", ForeignKey("project.id"), nullable=False),
    UniqueConstraint("timelog_id", "project_id",
                     name="idx_unique_timelog_project"),
)
