"""模型元数据仓储：静态数据."""

from app.domain.interfaces import ModelRepository
from app.domain.schemas import ModelInfo


class StaticModelRepository(ModelRepository):
    """静态模型元数据."""

    _DATA: list[ModelInfo] = [
        ModelInfo(
            id="qwen-image-2.0-pro",
            name="Qwen-Image-2.0-Pro",
            category="qwen",
            desc="文字渲染、真实质感、语义遵循能力更强",
            scenes=["复杂文字渲染", "写实人像", "精细细节"],
            output="512²~2048²，1~6 张",
            recommended=True,
            api_type="unified",
        ),
        ModelInfo(
            id="qwen-image-2.0",
            name="Qwen-Image-2.0",
            category="qwen",
            desc="加速版，兼顾效果与响应速度",
            scenes=["日常创作", "快速出图"],
            output="512²~2048²，1~6 张",
            recommended=True,
            api_type="unified",
        ),
        ModelInfo(
            id="qwen-image-max",
            name="Qwen-Image-Max",
            category="qwen",
            desc="真实感、自然度更强，AI 合成痕迹更低",
            scenes=["追求真实感", "人物质感"],
            output="固定 1 张，固定比例",
            recommended=False,
            api_type="unified",
        ),
        ModelInfo(
            id="qwen-image-plus",
            name="Qwen-Image-Plus",
            category="qwen",
            desc="擅长多样化艺术风格与文字渲染",
            scenes=["艺术风格", "插画", "文字海报"],
            output="固定 1 张",
            recommended=False,
            api_type="unified",
        ),
        ModelInfo(
            id="z-image-turbo",
            name="Z-Image-Turbo",
            category="z-image",
            desc="轻量级快速生图，支持中英文字渲染",
            scenes=["快速出图", "批量生成", "成本敏感"],
            output="512²~2048²，固定 1 张",
            recommended=False,
            api_type="unified",
        ),
        ModelInfo(
            id="wan2.6-t2i",
            name="万相 2.6",
            category="wan",
            desc="万相最新版，支持自由尺寸，宽高比 1:4~4:1",
            scenes=["超长图", "竖屏海报", "横屏 banner"],
            output="1280²~1440²，1~4 张",
            recommended=True,
            api_type="unified",
        ),
    ]

    def get_all(self) -> list[ModelInfo]:
        """返回所有模型."""
        return list(self._DATA)
