"""配置管理：从环境变量加载，业务代码不直接读取 os.getenv."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置."""

    dashscope_api_key: str = ""
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/api/v1"
    image_model: str = "qwen-image-2.0-pro"
    default_size: str = "1024*1024"
    default_negative_prompt: str = (
        "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，"
        "人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。"
    )
    request_timeout: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """获取配置单例."""
    return Settings()
