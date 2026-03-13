# Text2Image 项目规划方案

> 整合最新需求：多模型可选、模型介绍页面、优化架构。形成可执行的 To-Do List。

---

## 一、项目概述

### 1.1 目标

基于阿里云 DashScope API 的文生图 Web 应用，支持多模型可选，提供模型介绍页面，一键部署运行。

### 1.2 核心原则

- 不部署模型，全部调用云 API
- 代码最少，容易扩展
- 多模型可选（统一接口模型优先）
- 模型介绍页面供用户了解各模型特点

### 1.3 技术栈

| 模块 | 技术 |
|------|------|
| 图像生成 | Qwen-Image / 万相 / Z-Image / FLUX（阿里云 DashScope） |
| 服务框架 | FastAPI |
| 前端 | HTML + JS（含模型介绍页） |
| 部署 | Docker |

---

## 二、页面规划

### 2.1 页面结构

| 页面 | 路径 | 说明 |
|------|------|------|
| 首页（生成） | `/` 或 `index.html` | 输入 prompt、选择模型、生成图片 |
| 模型介绍 | `/models.html` 或 `models` | 各模型特点、适用场景、参数说明 |

### 2.2 模型介绍页内容（供前端使用）

以下内容可直接用于模型介绍页的展示数据，建议做成 JSON 或静态数据供前端渲染。

---

#### 2.2.1 Qwen-Image 文生图系列

| 模型 ID | 展示名称 | 简介 | 适用场景 | 输出规格 | 推荐度 |
|---------|----------|------|----------|----------|--------|
| qwen-image-2.0-pro | Qwen-Image-2.0-Pro | 千问图像生成与编辑 Pro 系列。文字渲染、真实质感、语义遵循能力更强。 | 复杂文字渲染、写实人像、精细细节 | 512²~2048²，1~6 张 | ⭐⭐⭐ 推荐 |
| qwen-image-2.0 | Qwen-Image-2.0 | 加速版，兼顾效果与响应速度。 | 日常创作、快速出图 | 512²~2048²，1~6 张 | ⭐⭐⭐ 推荐 |
| qwen-image-max | Qwen-Image-Max | 真实感、自然度更强，AI 合成痕迹更低。 | 追求真实感、人物质感 | 固定 1 张，固定比例 | ⭐⭐ |
| qwen-image-plus | Qwen-Image-Plus | 擅长多样化艺术风格与文字渲染。 | 艺术风格、插画、文字海报 | 固定 1 张 | ⭐⭐ |

**共同特性**：支持 `prompt_extend` 智能改写、`negative_prompt` 反向提示词、中英文输入。

---

#### 2.2.2 万相 Wan-T2I 系列

| 模型 ID | 展示名称 | 简介 | 适用场景 | 输出规格 | 推荐度 |
|---------|----------|------|----------|----------|--------|
| wan2.6-t2i | 万相 2.6 | 万相最新版，支持自由尺寸，宽高比 1:4~4:1。 | 超长图、竖屏海报、横屏 banner | 1280²~1440²，1~4 张 | ⭐⭐⭐ 推荐 |

**特性**：同步接口，一次请求返回结果。支持超长比例（如 768×2700）。

---

#### 2.2.3 Z-Image 系列

| 模型 ID | 展示名称 | 简介 | 适用场景 | 输出规格 | 推荐度 |
|---------|----------|------|----------|----------|--------|
| z-image-turbo | Z-Image-Turbo | 轻量级快速生图模型，支持中英文字渲染。 | 快速出图、批量生成、成本敏感 | 512²~2048²，固定 1 张 | ⭐⭐ |

**特性**：响应快，`prompt_extend` 可选（开启会增加耗时和费用）。

---

#### 2.2.4 FLUX 系列（阿里直供）

| 模型 ID | 展示名称 | 简介 | 适用场景 | 限制 | 推荐度 |
|---------|----------|------|----------|------|--------|
| flux-merged | FLUX-Merged | 结合 Dev 深度与 Schnell 速度，质量与速度兼顾。 | 高质量创意图像 | 仅北京地域，免费体验需申请 | ⭐⭐⭐ |
| flux-schnell | FLUX-Schnell | 少步模型，速度快，质量高。 | 快速出图、高并发 | 同上 | ⭐⭐ |
| flux-dev | FLUX-Dev | 面向非商业应用，质量接近专业版。 | 非商业项目 | 同上 | ⭐⭐ |

**注意**：FLUX 免费额度用完后不可付费续用，需单独申请审核。

---

### 2.3 模型介绍页 API 设计

为便于前端统一获取模型列表与介绍，可提供接口：

**GET /api/models**

返回示例：

```json
{
  "models": [
    {
      "id": "qwen-image-2.0-pro",
      "name": "Qwen-Image-2.0-Pro",
      "category": "qwen",
      "desc": "文字渲染、真实质感、语义遵循能力更强",
      "scenes": ["复杂文字渲染", "写实人像", "精细细节"],
      "output": "512²~2048²，1~6 张",
      "recommended": true,
      "api_type": "unified"
    }
  ]
}
```

`api_type`：`unified`（统一接口）| `flux`（需单独适配，二期）

---

## 三、系统架构

### 3.1 流程

```
用户输入 prompt + 选择模型
      │
      ▼
FastAPI 接收请求
      │
      ▼
调用 DashScope multimodal-generation（或 FLUX image-synthesis）
  - model 参数由前端传入
  - prompt_extend、size、negative_prompt 等可配置
      │
      ▼
获得图片 URL
      │
      ▼
返回前端显示
```

### 3.2 项目目录结构（低耦合、高内聚）

> 详细架构说明见 `docs/ARCHITECTURE.md`

```
text2image/
│
├── app/
│   ├── main.py                    # 应用入口
│   │
│   ├── api/                       # API 层：路由、参数校验
│   │   ├── deps.py                # 依赖注入
│   │   └── v1/
│   │       ├── router.py          # 路由聚合
│   │       ├── generate.py        # POST /api/v1/generate
│   │       └── models.py          # GET /api/v1/models
│   │
│   ├── core/                      # 核心：配置、常量
│   │   ├── config.py
│   │   └── constants.py
│   │
│   ├── domain/                    # 领域层：数据结构、接口
│   │   ├── schemas.py             # 请求/响应模型
│   │   ├── models.py              # 领域模型
│   │   └── interfaces.py         # ImageGenerator 等抽象
│   │
│   ├── services/                  # 服务层：业务编排
│   │   ├── image_service.py
│   │   └── model_service.py
│   │
│   └── infrastructure/            # 基础设施：外部依赖
│       ├── dashscope/
│       │   ├── client.py          # HTTP 客户端
│       │   └── adapter.py         # 实现 ImageGenerator
│       └── data/
│           └── model_repository.py # 模型元数据
│
├── static/
│   ├── index.html
│   └── models.html
│
├── tests/
├── docs/
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## 四、API 设计

> 路径采用 `/api/v1/` 前缀，便于后续版本演进。

### 4.1 POST /api/v1/generate

**请求**：

```json
{
  "prompt": "cyberpunk city at night",
  "model": "qwen-image-2.0-pro",
  "prompt_extend": true,
  "size": "1024*1024",
  "negative_prompt": "低分辨率，低画质",
  "n": 1
}
```

| 字段 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| prompt | string | 是 | - | ≤800 字符 |
| model | string | 否 | qwen-image-2.0-pro | 模型 ID |
| prompt_extend | bool | 否 | true | 智能改写 |
| size | string | 否 | 1024*1024 | 分辨率 |
| negative_prompt | string | 否 | 默认值 | 反向提示词 |
| n | int | 否 | 1 | 2.0 系列可 1~6 |

**响应**：

```json
{
  "prompt": "用户输入",
  "image": "https://...",
  "request_id": "xxx",
  "usage": { "width": 1024, "height": 1024, "image_count": 1 }
}
```

### 4.2 GET /api/v1/models

返回可选模型列表及介绍（见 2.3）。

### 4.3 GET /health

`{"status": "ok"}`

---

## 五、To-Do List（开发任务）

### Phase 1：基础框架（MVP）

- [ ] **1.1** 初始化项目：目录结构（按 ARCHITECTURE.md）、requirements.txt、.env.example
- [ ] **1.2** 实现 `core/config.py`、`core/constants.py`
- [ ] **1.3** 实现 `domain/schemas.py`、`domain/interfaces.py`
- [ ] **1.4** 实现 `infrastructure/dashscope/client.py`、`adapter.py`
- [ ] **1.5** 实现 `services/image_service.py`
- [ ] **1.6** 实现 `api/deps.py`、`api/v1/generate.py`、`router.py`
- [ ] **1.7** 实现 `main.py`：挂载路由、`GET /health`
- [ ] **1.8** 实现 `index.html`：输入框、模型下拉、生成按钮、图片展示
- [ ] **1.9** Dockerfile + README.md

### Phase 2：模型介绍页

- [ ] **2.1** 实现 `infrastructure/data/model_repository.py`：模型元数据
- [ ] **2.2** 实现 `services/model_service.py`
- [ ] **2.3** 实现 `api/v1/models.py`、`GET /api/v1/models`
- [ ] **2.4** 实现 `models.html`：展示模型介绍
- [ ] **2.5** 首页增加「模型介绍」入口

### Phase 3：体验优化

- [ ] **3.1** 前端模型下拉从 `/api/v1/models` 动态加载
- [ ] **3.2** 加载状态、错误提示、超时处理
- [ ] **3.3** 根据模型调整 size 可选值（可选）

### Phase 4：扩展（可选）

- [ ] **4.1** FLUX：新增 `infrastructure/flux/adapter.py` 实现 ImageGenerator
- [ ] **4.2** 万相异步模型
- [ ] **4.3** 图像持久化
- [ ] **4.4** 历史记录（SQLite）

---

## 六、开发顺序建议

| 顺序 | 任务 | 预估时间 |
|------|------|----------|
| 1 | 1.1 ~ 1.5 后端基础 | 1h |
| 2 | 1.6 首页、1.7 Docker | 30min |
| 3 | 2.1 ~ 2.4 模型介绍页 | 45min |
| 4 | 3.1 ~ 3.4 体验优化 | 30min |

**MVP 可交付**：完成 Phase 1 + Phase 2 即可。

---

## 七、环境变量

```env
# 必填
DASHSCOPE_API_KEY=sk-xxx

# 可选
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/api/v1
IMAGE_MODEL=qwen-image-2.0-pro
```

---

## 八、参考文档

- `docs/ARCHITECTURE.md` - **系统架构设计（低耦合、高内聚）**
- `docs/architecture-optimization.md` - 架构优化说明
- `docs/aliyun-models-comparison.md` - 模型对比与 API 可选用性
- `docs/aliyun-qwen-text2img.md` - Qwen-Image API 详细文档
