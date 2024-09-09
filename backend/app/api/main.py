from fastapi import APIRouter

from app.api.routes import project, task

api_router = APIRouter()

api_router.include_router(project.router, tags=["project"], prefix="/project")
api_router.include_router(task.router, tags=["task"], prefix="/task")

