from app.cruds.base import CRUDBase
from app.models.task import Task
from sqlmodel import Session
from datetime import datetime
from app.models import TaskStatus
from app import cruds


class CRUDTask(CRUDBase[Task]):
    def get_tasks_by_project_id(self, session, project_id):
        return session.query(Task).filter(Task.project_id == project_id).all()
    
    def get_status_update(
            self,
            session: Session,
            obj_current: Task,
            internal_commit=False  # Указываем, нужен ли коммит внутри транзакции
    ):
        if obj_current.due_date and obj_current.due_date.timestamp() < datetime.now().timestamp():
            obj_current = cruds.task.update(
                session=session,
                obj_current=obj_current,
                obj_new=dict(status=TaskStatus.OVERDUE),
            )
            if internal_commit:
                session.commit()
        return obj_current

    def get_tasks_by_project_id_with_update(
            self, 
            session: Session, 
            project_id: int, 
            filters: list | None = None,
            skip: int = 0,
            limit: int = 100
        ):
        tasks = cruds.task.get_list(
            session=session,
            filters=[Task.project_id == project_id] + (filters or []),
            skip=skip,
            limit=limit
        )
        if not tasks:
           return [] 
        updated_tasks = [
            cruds.task.get_status_update(session, task, internal_commit=False) for task in tasks
        ]
        session.commit()
        return updated_tasks


task = CRUDTask(Task)
