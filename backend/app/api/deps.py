from collections.abc import Generator
from datetime import datetime
from fastapi import Depends, Query, HTTPException
from sqlmodel import Session

from app.core.engine import engine
from app.models import Task, TaskStatus
from app.models.utils import Pagination

# from app.models.user import TokenPayload, User

# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/login/access-token"
# )


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def pagination(
    skip: int = 0,
    limit: int = 100,
) -> Pagination:
    if skip < 0 or limit <=0:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    return Pagination(skip=skip, limit=limit)


def get_status_filter(
    status: TaskStatus | None = Query(None, title="Status", description="Filter tasks by status")
):
    if not status:
        return []
    return [Task.status == status]

def get_due_date_filter(
    due_date_from: str | None = Query(None, title="Due Date From", description="Filter tasks by due date from"),
    due_date_to: str | None = Query(None, title="Due Date To", description="Filter tasks by due date to")
):
    filters = []
    try:
        if due_date_from:
            due_date_from = datetime.fromisoformat(due_date_from)
            filters.append(Task.due_date >= due_date_from)
        if due_date_to:
            due_date_to = datetime.fromisoformat(due_date_to)
            filters.append(Task.due_date <= due_date_to)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid due date format")
    return filters

def get_task_filters(
    status_filter: list | None = Depends(get_status_filter),
    due_date_filter: list | None = Depends(get_due_date_filter)
):
    filters = []
    if status_filter:
        filters.extend(status_filter)
    if due_date_filter:
        filters.extend(due_date_filter)
    return filters
