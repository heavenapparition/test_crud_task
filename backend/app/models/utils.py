from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import DateTime, Field, SQLModel, func


class TimeStampModel(SQLModel):
    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()},
    )


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class Pagination(BaseModel):
    skip: int = 0
    limit: int = 100

    class Config:
        schema_extra = {
            "example": {
                "skip": 0,
                "limit": 10
            }
        }
