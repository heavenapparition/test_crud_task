from datetime import datetime

from sqlmodel import DateTime, Field, SQLModel  # noqa

from app.models.utils import TaskStatus, TimeStampModel


class WorkBase(TimeStampModel):
    description: str = Field(..., max_length=255)


class TaskBase(WorkBase):
    title: str = Field(..., max_length=64)
    due_date: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True)
    )
    status: TaskStatus = Field(...)


class ProjectBase(WorkBase):
    name: str = Field(..., max_length=64)
