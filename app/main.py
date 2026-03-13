"""应用入口."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.v1.router import api_router

app = FastAPI(
    title="Text2Image",
    description="基于阿里云 DashScope 的文生图 API",
    version="0.1.0",
)

# 健康检查（必须在静态文件 mount 之前注册）
@app.get("/health")
def health():
    """健康检查."""
    return {"status": "ok"}

# API 路由
app.include_router(api_router, prefix="/api")

# 静态文件（最后挂载，避免覆盖 /api、/health）
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
