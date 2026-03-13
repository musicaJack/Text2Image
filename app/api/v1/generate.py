"""POST /api/v1/generate 文生图."""

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_image_service
from app.domain.schemas import GenerateRequest, GenerateResponse
from app.services.image_service import ImageService

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("", response_model=GenerateResponse)
def generate(
    request: GenerateRequest,
    service: ImageService = Depends(get_image_service),
) -> GenerateResponse:
    """根据文本生成图像."""
    try:
        return service.generate(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
