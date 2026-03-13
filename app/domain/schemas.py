"""请求/响应 Pydantic 模型."""

from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """文生图请求."""

    prompt: str = Field(..., min_length=1, max_length=800)
    model: str = Field(default="qwen-image-2.0-pro")
    prompt_extend: bool = Field(default=True)
    size: str = Field(default="1024*1024")
    negative_prompt: Optional[str] = Field(default=None, max_length=500)
    n: int = Field(default=1, ge=1, le=6)


class GenerateResponse(BaseModel):
    """文生图响应."""

    prompt: str
    image: str
    request_id: Optional[str] = None
    usage: Optional[dict] = None


class ModelInfo(BaseModel):
    """模型信息."""

    id: str
    name: str
    category: str
    desc: str
    scenes: list[str] = Field(default_factory=list)
    output: str = ""
    recommended: bool = False
    api_type: str = "unified"


class ModelsResponse(BaseModel):
    """模型列表响应."""

    models: list[ModelInfo]


class ErrorResponse(BaseModel):
    """错误响应."""

    error: dict
