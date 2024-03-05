from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimeLogBase(BaseModel):
    pass


class TimeLogGet(TimeLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_fk: int
    end_time: datetime | None = None
    start_time: datetime
    project_fk: int


class TimeLogCreate(TimeLogBase):
    project_fk: int
    
