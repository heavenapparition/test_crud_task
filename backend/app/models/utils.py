from datetime import datetime
from sqlmodel import Field, SQLModel, func, DateTime
from enum import Enum


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
