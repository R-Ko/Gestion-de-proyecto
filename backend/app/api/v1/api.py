from fastapi import APIRouter
from app.api.v1.routers import projects, tasks, comments, users, activities, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks.router, prefix="", tags=["tasks"])
api_router.include_router(comments.router, prefix="", tags=["comments"])
api_router.include_router(activities.router, prefix="", tags=["activities"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
