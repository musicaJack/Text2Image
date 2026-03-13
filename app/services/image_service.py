"""文生图业务编排."""

from app.core.constants import UNIFIED_MODELS
from app.domain.interfaces import ImageGenerator
from app.domain.schemas import GenerateRequest, GenerateResponse


class ImageService:
    """文生图服务."""

    def __init__(self, image_generator: ImageGenerator):
        self._generator = image_generator

    def generate(self, request: GenerateRequest) -> GenerateResponse:
        """生成图像：校验 model、调用生成器."""
        if request.model not in UNIFIED_MODELS:
            raise ValueError(f"不支持的模型: {request.model}")
        return self._generator.generate(request)
