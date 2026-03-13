"""DashScope 文生图适配器：实现 ImageGenerator 接口."""

from typing import Optional

from app.core.config import get_settings
from app.domain.interfaces import ImageGenerator
from app.domain.schemas import GenerateRequest, GenerateResponse
from app.infrastructure.dashscope.client import DashScopeClient


class DashScopeImageAdapter(ImageGenerator):
    """DashScope multimodal-generation 文生图适配器."""

    PATH = "/services/aigc/multimodal-generation/generation"

    def __init__(self, client: Optional[DashScopeClient] = None):
        self._client = client or DashScopeClient()
        self._config = get_settings()

    def generate(self, request: GenerateRequest) -> GenerateResponse:
        """调用 DashScope 同步接口生成图像."""
        negative_prompt = (
            request.negative_prompt
            or self._config.default_negative_prompt
        )
        payload = {
            "model": request.model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": request.prompt[:800]}],
                    }
                ],
            },
            "parameters": {
                "prompt_extend": request.prompt_extend,
                "watermark": False,
                "size": request.size,
                "negative_prompt": negative_prompt[:500],
                "n": request.n,
            },
        }
        data = self._client.post(self.PATH, payload)
        if data.get("code"):
            raise ValueError(data.get("message", "Unknown API error"))
        choice = data["output"]["choices"][0]
        content = choice["message"]["content"][0]
        image_url = content["image"]
        return GenerateResponse(
            prompt=request.prompt,
            image=image_url,
            request_id=data.get("request_id"),
            usage=data.get("usage"),
        )
