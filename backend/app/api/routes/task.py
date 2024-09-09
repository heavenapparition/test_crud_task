
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.project import *
from app import cruds
from app.api import deps
from app.models.task import CreateTask, TaskOut, UpdateTask
from app.models.utils import Pagination

router = APIRouter()

@router.get("/", response_model=list[TaskOut])
def get_tasks_by_project_id(
        project_id: int,
        session: Session = Depends(deps.get_db),
        pagination: Pagination = Depends(deps.pagination),
        task_filters: list | None = Depends(deps.get_task_filters)
):
    tasks = cruds.task.get_tasks_by_project_id_with_update(
        project_id=project_id,
        session=session,
        filters=task_filters,
        skip=pagination.skip,
        limit=pagination.limit
        )
    return tasks


@router.post("/", response_model=TaskOut)
def create_task(
        task_on_creation: CreateTask,
        project_id: int,
        session: Session = Depends(deps.get_db),
):
    project = cruds.project.get_one_by_id(session=session, id=project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    task = cruds.task.create(
        session=session,
        obj_in=dict(project_id=project_id, **task_on_creation.dict())
    )
    cruds.task.get_status_update(
        session=session,
        obj_current=task,
        internal_commit=False
    )
    session.commit()
    return task


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
        task_id: int,
        task_on_update: UpdateTask,
        session: Session = Depends(deps.get_db)
):
    task = cruds.task.get_one_by_id(session=session, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    cruds.task.update(
        session=session,
        obj_current=task,
        obj_new=task_on_update
    )
    cruds.task.get_status_update(
        session=session,
        obj_current=task,
        internal_commit=False
    )
    session.commit()
    return task


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
        task_id: int,
        session: Session = Depends(deps.get_db),
):
    task = cruds.task.get_one_by_id(
        session=session,
        id=task_id
    )
    task = cruds.task.get_status_update(
        session=session,
        obj_current=task,
        internal_commit=True
    )
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task
