"""抽象接口：便于替换实现、Mock 测试."""

from abc import ABC, abstractmethod

from app.domain.schemas import GenerateRequest, GenerateResponse, ModelInfo


class ImageGenerator(ABC):
    """文生图能力抽象."""

    @abstractmethod
    def generate(self, request: GenerateRequest) -> GenerateResponse:
        """根据请求生成图像."""
        pass


class ModelRepository(ABC):
    """模型元数据仓储."""

    @abstractmethod
    def get_all(self) -> list[ModelInfo]:
        """获取所有模型信息."""
        pass
