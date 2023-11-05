from fastapi import APIRouter

from app.api.api_v1.endpoints import health, user

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
