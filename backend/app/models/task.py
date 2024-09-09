from datetime import datetime

from sqlmodel import DateTime, Field, Relationship, SQLModel

from app.models import *
from app.models.base import TaskBase
from app.models.utils import TaskStatus


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_id: int | None = Field(foreign_key="project.id")
    project: Project = Relationship(back_populates="tasks")


class CreateTask(SQLModel):
    title: str = Field(..., max_length=64)
    due_date: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True)
    )
    status: TaskStatus = Field(...)
    description: str = Field(..., max_length=255)


class TaskOut(TaskBase):
    id: int


class UpdateTask(SQLModel):
    description: str | None = Field(..., max_length=255)
    title: str | None = Field(..., max_length=64)
    due_date: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True)
    )
    status: TaskStatus = Field(...)
