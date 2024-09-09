
from sqlmodel import Field, Relationship

from .base import ProjectBase, SQLModel


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tasks: list["Task"] | None = Relationship(back_populates="project")


class ProjectOut(ProjectBase):
    id: int


class UpdateProject(SQLModel):
    description: str | None = Field(None, max_length=255)
    name: str | None = Field(None, max_length=64)


class CreateProject(SQLModel):
    description: str = Field(..., max_length=255)
    name: str = Field(..., max_length=64)


