"""依赖注入."""

from functools import lru_cache

from app.core.config import Settings, get_settings
from app.domain.interfaces import ImageGenerator, ModelRepository
from app.infrastructure.dashscope.adapter import DashScopeImageAdapter
from app.infrastructure.dashscope.client import DashScopeClient
from app.infrastructure.data.model_repository import StaticModelRepository
from app.services.image_service import ImageService
from app.services.model_service import ModelService


def get_config() -> Settings:
    """获取配置."""
    return get_settings()


@lru_cache
def get_image_generator() -> ImageGenerator:
    """获取文生图实现."""
    return DashScopeImageAdapter(DashScopeClient())


@lru_cache
def get_model_repository() -> ModelRepository:
    """获取模型仓储."""
    return StaticModelRepository()


def get_image_service() -> ImageService:
    """获取文生图服务."""
    return ImageService(get_image_generator())


def get_model_service() -> ModelService:
    """获取模型服务."""
    return ModelService(get_model_repository())
