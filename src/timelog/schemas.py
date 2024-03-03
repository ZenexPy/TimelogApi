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


class TimeLogCreate(TimeLogBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'message': "Execute endpoint to open timelog record"
                }
            ]
        }
    }
