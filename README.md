# Text2Image

基于阿里云 DashScope API 的文生图 Web 应用，支持多模型可选。

## 快速开始

### 1. 环境变量

复制 `.env.example` 为 `.env`，填写 API Key：

```bash
cp .env.example .env
# 编辑 .env，设置 DASHSCOPE_API_KEY=sk-xxx
```

### 2. 本地运行

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问 http://localhost:8000

### 3. Docker Compose 运行（推荐）

```bash
# 确保 .env 中已配置 DASHSCOPE_API_KEY
docker-compose up -d
```

访问 http://localhost:8000

### 4. 单容器 Docker 运行

```bash
docker build -t text2image .
docker run -p 8000:8000 -e DASHSCOPE_API_KEY=sk-xxx text2image
```

## API

| 接口 | 说明 |
|------|------|
| `POST /api/v1/generate` | 文生图 |
| `GET /api/v1/models` | 模型列表 |
| `GET /health` | 健康检查 |

## 架构说明

- **后端**：FastAPI，提供 REST API（`/api/v1/*`）
- **前端**：静态 HTML/JS（`static/`），由 FastAPI 一并托管
- 前后端同域部署，无需 CORS

## 页面

- `/` - 首页（生成）
- `/models.html` - 模型介绍

## 架构

低耦合、高内聚分层架构，详见 `docs/ARCHITECTURE.md`。
