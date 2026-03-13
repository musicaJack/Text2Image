"""v1 路由聚合."""

from fastapi import APIRouter

from app.api.v1 import generate, models

api_router = APIRouter(prefix="/v1")
api_router.include_router(generate.router, prefix="")
api_router.include_router(models.router, prefix="")
