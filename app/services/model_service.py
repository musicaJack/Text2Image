"""模型列表业务."""

from typing import Optional

from app.domain.interfaces import ModelRepository
from app.domain.schemas import ModelInfo


class ModelService:
    """模型服务."""

    def __init__(self, repository: ModelRepository):
        self._repo = repository

    def list_models(self, api_type: Optional[str] = "unified") -> list[ModelInfo]:
        """获取模型列表，可按 api_type 过滤."""
        all_models = self._repo.get_all()
        if api_type:
            return [m for m in all_models if m.api_type == api_type]
        return all_models
