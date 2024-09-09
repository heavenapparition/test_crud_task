
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import cruds
from app.api import deps
from app.models.project import *
from app.models.utils import Pagination

router = APIRouter()

@router.get("/", response_model=list[ProjectOut])
def get_projects(
    session: Session = Depends(deps.get_db),
    pagination: Pagination = Depends(deps.pagination)
) -> list[ProjectOut]:
    """
    Получение списка всех проектов

    Args:
        session: сессия БД
        pagination: параметры пагинации

    Returns:
        список проектов
    """
    projects = cruds.project.get_list(
        session=session,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return projects


@router.post("/", response_model=ProjectOut)
def create_project(
        project_on_creation: CreateProject,
        session: Session = Depends(deps.get_db),
):
    project = cruds.project.create(
        session=session,
        obj_in=project_on_creation
    )
    session.commit()
    return project


@router.patch("/", response_model=ProjectOut)
def update_project(
        project_id: int,
        project_on_update: UpdateProject,
        session: Session = Depends(deps.get_db)
):
    project = cruds.project.get_one_by_id(session=session, id=project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    cruds.project.update(
        session=session,
        obj_current=project,
        obj_new=project_on_update
    )
    session.commit()
    return project


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
        project_id: int,
        session: Session = Depends(deps.get_db),
):
    project = cruds.project.get_one_by_id(
        session=session,
        id=project_id
    )
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return project
