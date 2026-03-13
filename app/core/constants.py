"""常量定义：默认值、限制等."""

MAX_PROMPT_LEN = 800
MAX_NEGATIVE_PROMPT_LEN = 500
MAX_IMAGES = 6
MIN_IMAGES = 1

# 统一接口支持的模型（multimodal-generation）
UNIFIED_MODELS = frozenset({
    "qwen-image-2.0-pro",
    "qwen-image-2.0",
    "qwen-image-max",
    "qwen-image-plus",
    "qwen-image",
    "z-image-turbo",
    "wan2.6-t2i",
})
