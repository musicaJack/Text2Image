# Text2Image MVP 方案优化（系统架构与软件工程视角）

> 基于 `intro.md` 的规划，结合 `aliyun-qwen-text2img.md` 中 Qwen-Image API 的特性，从系统架构和软件工程角度进行优化与完善。

---

## 一、核心发现：架构可大幅简化

### 1.1 原方案 vs 实际能力

| 维度 | intro.md 原方案 | Qwen-Image API 实际能力 |
|------|-----------------|--------------------------|
| **Prompt 优化** | 单独调用 Qwen 文本模型（text-generation） | **内置 `prompt_extend` 参数**，模型自动优化与润色 |
| **图像生成** | Wanx API（`text2image/image-synthesis`） | Qwen-Image API（`multimodal-generation/generation`） |
| **API 调用次数** | 2 次（Qwen + Wanx） | **1 次**（Qwen-Image 一站式） |
| **API Key** | 可能需区分 | 同一 DashScope API Key |

### 1.2 优化结论

**Qwen-Image 已内置 prompt 智能改写**，无需再单独调用 Qwen 文本模型。架构可简化为：

```
用户输入 → FastAPI → Qwen-Image API（prompt_extend=true）→ 返回图片 URL
```

**收益**：减少一次网络调用、降低延迟、降低成本、代码更简洁。

---

## 二、优化后的技术方案

### 2.1 技术选型（更新）

| 模块 | 技术 | 作用 |
|------|------|------|
| 图像生成 | **Qwen-Image API**（替代 Wanx） | 文生图 + 内置 prompt 优化 |
| 服务框架 | FastAPI | 提供 API |
| 部署 | Docker | 一键运行 |
| 前端 | HTML + JS | 简单 UI |

**移除**：独立的 Qwen 文本模型调用（由 `prompt_extend` 替代）。

### 2.2 系统流程（优化后）

```
用户输入文本
      │
      ▼
FastAPI 接收请求
      │
      ▼
调用 Qwen-Image API（multimodal-generation）
  - 传入用户 prompt
  - prompt_extend=true（内置优化）
  - 可选：negative_prompt、size、n
      │
      ▼
获得图片 URL（及 actual_prompt）
      │
      ▼
返回前端显示
```

### 2.3 系统架构图（优化后）

```
Browser
   │
   ▼
FastAPI server
   │
   └── Qwen-Image API（multimodal-generation）
           ├── prompt 优化（prompt_extend）
           └── 图像生成
```

---

## 三、Qwen-Image API 关键特性与设计决策

### 3.1 必须关注的特性

| 特性 | 说明 | 设计建议 |
|------|------|----------|
| **地域隔离** | 北京 / 新加坡 有独立 API Key 和请求地址 | 配置化：`DASHSCOPE_API_KEY` + `DASHSCOPE_BASE_URL` |
| **URL 有效期** | 图像链接仅保留 24 小时 | 若需持久化，需下载并转存 OSS/S3 |
| **prompt_extend** | 默认 true，模型自动优化 prompt | MVP 保持开启；高级用户可提供开关 |
| **模型选择** | qwen-image-2.0-pro（推荐）、qwen-image-2.0 等 | 配置化，便于切换 |
| **同步 vs 异步** | 2.0 系列仅同步；plus/image 支持异步 | MVP 用同步接口，实现简单 |

### 3.2 推荐模型选择

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| MVP / 默认 | `qwen-image-2.0-pro` | 文字渲染、真实质感、语义遵循更强 |
| 追求速度 | `qwen-image-2.0` | 加速版，效果与性能平衡 |
| 多图生成 | `qwen-image-2.0-pro` | 支持 n=1~6 |

### 3.3 请求地址

- **北京**：`https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **新加坡**：`https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

---

## 四、项目目录结构（优化版）

```
text2image-mvp/
│
├── app/
│   ├── main.py          # FastAPI 入口
│   ├── image.py         # Qwen-Image API 封装（替代原 qwen.py + image.py）
│   ├── config.py        # 配置管理（模型、地域、参数）
│   └── schemas.py       # Pydantic 模型（请求/响应）
│
├── static/
│   └── index.html
│
├── requirements.txt
├── Dockerfile
├── .env.example         # 环境变量模板
└── README.md
```

**变更说明**：
- 合并 `qwen.py` 与 `image.py` 为 `image.py`（单一职责：调用 Qwen-Image）
- 新增 `schemas.py` 统一请求/响应结构
- 新增 `config.py` 集中管理可配置项

---

## 五、API 设计（优化版）

### 5.1 生成图片

**接口**：`POST /generate`

**请求**：

```json
{
  "prompt": "cyberpunk city",
  "prompt_extend": true,
  "size": "1024*1024",
  "negative_prompt": "低分辨率，低画质，肢体畸形"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 用户输入，≤800 字符 |
| prompt_extend | bool | 否 | 默认 true，开启智能改写 |
| size | string | 否 | 默认 1024*1024，2.0 系列支持 512²~2048² |
| negative_prompt | string | 否 | 反向提示词，≤500 字符 |
| n | int | 否 | 2.0 系列可 1~6，默认 1 |

**响应**：

```json
{
  "prompt": "用户原始输入",
  "actual_prompt": "模型优化后的实际 prompt（prompt_extend 开启时返回）",
  "image": "https://dashscope-result-xxx.oss-cn-xxx.aliyuncs.com/xxx.png?Expires=xxx",
  "request_id": "xxx",
  "usage": {
    "width": 1024,
    "height": 1024,
    "image_count": 1
  }
}
```

### 5.2 健康检查

`GET /health` → `{"status": "ok"}`

### 5.3 错误响应规范

```json
{
  "error": {
    "code": "InvalidParameter",
    "message": "错误描述",
    "request_id": "xxx"
  }
}
```

---

## 六、配置管理（config.py）

```python
# config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 必填
    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    
    # 可选，支持北京/新加坡
    dashscope_base_url: str = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/api/v1"
    )
    
    # 模型与默认参数
    image_model: str = os.getenv("IMAGE_MODEL", "qwen-image-2.0-pro")
    default_size: str = "1024*1024"
    default_negative_prompt: str = "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 七、核心代码逻辑（image.py）

```python
# image.py
import requests
from app.config import settings

def generate_image(
    prompt: str,
    *,
    prompt_extend: bool = True,
    size: str = None,
    negative_prompt: str = None,
    n: int = 1,
) -> dict:
    """
    调用 Qwen-Image 同步接口，一站式完成 prompt 优化 + 图像生成。
    """
    url = f"{settings.dashscope_base_url.rstrip('/')}/services/aigc/multimodal-generation/generation"
    
    payload = {
        "model": settings.image_model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt[:800]}]  # 超长截断
                }
            ]
        },
        "parameters": {
            "prompt_extend": prompt_extend,
            "watermark": False,
            "size": size or settings.default_size,
            "negative_prompt": negative_prompt or settings.default_negative_prompt,
            "n": n,
        }
    }
    
    headers = {
        "Authorization": f"Bearer {settings.dashscope_api_key}",
        "Content-Type": "application/json",
    }
    
    r = requests.post(url, json=payload, headers=headers, timeout=60)
    data = r.json()
    
    if r.status_code != 200 or "code" in data and data["code"]:
        raise ValueError(data.get("message", "Unknown error"))
    
    choice = data["output"]["choices"][0]
    content = choice["message"]["content"][0]
    image_url = content["image"]
    
    return {
        "image": image_url,
        "request_id": data.get("request_id"),
        "usage": data.get("usage", {}),
    }
```

**说明**：同步接口不返回 `actual_prompt`，若业务需要可考虑异步接口（仅 plus/image 支持）或接受该限制。

---

## 八、软件工程优化建议

### 8.1 分层与职责

| 层 | 职责 | 示例 |
|----|------|------|
| API 层 | 路由、参数校验、错误处理 | main.py |
| 服务层 | 业务逻辑、调用外部 API | image.py |
| 配置层 | 环境变量、默认值 | config.py |
| 模型层 | 请求/响应结构 | schemas.py |

### 8.2 错误处理

- 统一捕获 `requests` 超时、连接错误
- 解析 DashScope 返回的 `code`、`message`
- 返回结构化错误，便于前端展示与排查

### 8.3 可观测性

- 记录 `request_id`，便于阿里云侧排查
- 可选：接入日志（如 structlog）、简单 metrics（请求数、耗时）

### 8.4 安全

- API Key 仅通过环境变量注入，不落库、不写死
- 对用户 prompt 做长度限制（≤800）
- 若对外暴露，建议加限流、鉴权

### 8.5 扩展性预留

| 未来需求 | 实现方式 |
|----------|----------|
| 图像持久化 | 下载 URL 后上传 OSS/S3，返回持久链接 |
| 历史记录 | SQLite / 数据库 |
| 异步任务 | 使用 qwen-image-plus 异步接口 + 轮询/回调 |
| 多模型切换 | config 中 `IMAGE_MODEL` 可配置 |
| 用户登录 | JWT + 中间件 |

---

## 九、Docker 部署（更新）

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**requirements.txt**：

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
requests>=2.31.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
```

**运行**：

```bash
docker run -p 8000:8000 \
  -e DASHSCOPE_API_KEY=sk-xxx \
  -e DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/api/v1 \
  text2image
```

---

## 十、开发时间评估（更新）

| 步骤 | 原估计 | 优化后 | 说明 |
|------|--------|--------|------|
| FastAPI 接口 | 30 分钟 | 25 分钟 | 少一个依赖调用 |
| Qwen 调用 | 10 分钟 | — | 已移除 |
| Wanx/Qwen-Image 调用 | 10 分钟 | 15 分钟 | 改用 multimodal-generation |
| 配置与错误处理 | — | 15 分钟 | 新增 |
| HTML 页面 | 20 分钟 | 20 分钟 | 不变 |
| Docker 部署 | 20 分钟 | 15 分钟 | 依赖更少 |

**总时间**：约 1.5~2 小时完成 MVP。

---

## 十一、方案对比总结

| 维度 | 原方案（intro.md） | 优化方案 |
|------|--------------------|----------|
| API 调用链 | Qwen 文本 + Wanx 图像 | 仅 Qwen-Image |
| 代码复杂度 | 2 个 API 模块 | 1 个 API 模块 |
| 延迟 | 2 次网络往返 | 1 次 |
| 成本 | 文本 + 图像双计费 | 仅图像计费 |
| 可配置性 | 较弱 | 地域、模型、参数可配置 |
| 错误处理 | 基础 | 结构化错误、request_id 透传 |
| 扩展路径 | 清晰 | 保持清晰，并预留配置与分层 |

---

## 十二、实施建议

1. **优先采用 Qwen-Image 同步接口**，实现简单、延迟可接受。
2. **默认开启 `prompt_extend`**，减少用户写 prompt 负担。
3. **配置化地域与模型**，便于后续切换或 A/B 测试。
4. **明确图像 URL 24 小时有效期**，若产品需要长期保存，尽早设计下载 + 存储流程。
5. **保留原 intro.md 中的扩展规划**（历史记录、用户登录、OSS 等），在架构上预留接口即可。
