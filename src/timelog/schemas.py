from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):

    secret_name: str


class Project(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProjectGet(Project):

    started_at: datetime


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    started_at: datetime


class ProjectUpdatePartial(ProjectBase):
    secret_name: str | None = None
    started_at: datetime | None = None



