from fastapi import APIRouter

from app.api.routes import project

api_router = APIRouter()

api_router.include_router(project.router, tags=["project"])
