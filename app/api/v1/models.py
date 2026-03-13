"""GET /api/v1/models 模型列表."""

from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_model_service
from app.domain.schemas import ModelsResponse
from app.services.model_service import ModelService

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=ModelsResponse)
def list_models(
    api_type: Optional[str] = Query(default="unified", description="unified | flux | 空=全部"),
    service: ModelService = Depends(get_model_service),
) -> ModelsResponse:
    """获取可选模型列表及介绍."""
    models = service.list_models(api_type=api_type or None)
    return ModelsResponse(models=models)
