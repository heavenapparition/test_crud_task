from typing import Optional, List
from sqlmodel import Field, Relationship, DateTime
from .base import ProjectBase, SQLModel


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["Task"] | None = Relationship(back_populates="project")


class ProjectOut(ProjectBase):
    id: int


class UpdateProject(SQLModel):
    description: Optional[str] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=64)


class CreateProject(SQLModel):
    description: str = Field(..., max_length=255)
    name: str = Field(..., max_length=64)


