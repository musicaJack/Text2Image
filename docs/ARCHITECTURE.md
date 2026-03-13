# Text2Image 系统架构设计

> 遵循**低耦合、高内聚**原则，采用分层架构与依赖倒置，便于扩展与维护。

---

## 一、架构原则

### 1.1 低耦合（Low Coupling）

- **模块间依赖单向流动**：上层依赖下层，下层不依赖上层
- **面向接口编程**：外部依赖（如 DashScope API）通过抽象接口接入，可替换
- **配置与逻辑分离**：配置集中管理，业务代码不直接读取环境变量
- **路由与业务分离**：API 层只做参数校验与响应封装，不包含业务逻辑

### 1.2 高内聚（High Cohesion）

- **单一职责**：每个模块只负责一类事务
- **相关代码聚合**：同一领域/功能的代码放在同一模块
- **按能力分层**：API 层、服务层、领域层、基础设施层职责清晰

---

## 二、分层架构

```
┌─────────────────────────────────────────────────────────────┐
│  API Layer (api/)          ← HTTP 入口、路由、参数校验        │
├─────────────────────────────────────────────────────────────┤
│  Service Layer (services/)  ← 业务编排、流程控制               │
├─────────────────────────────────────────────────────────────┤
│  Domain Layer (domain/)     ← 数据结构、接口定义、常量        │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (infrastructure/)  ← 外部 API、数据源   │
└─────────────────────────────────────────────────────────────┘

依赖方向：API → Service → Domain
         Service → Infrastructure（通过 Domain 定义的接口）
         Infrastructure → Domain（实现接口）
```

---

## 三、目录结构

```
text2image/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # 应用入口，挂载路由
│   │
│   ├── api/                       # 【API 层】HTTP 入口
│   │   ├── __init__.py
│   │   ├── deps.py                # 依赖注入（config、services）
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py          # 聚合 v1 路由
│   │       ├── generate.py        # POST /generate
│   │       └── models.py          # GET /models
│   │
│   ├── core/                      # 【核心】配置与常量
│   │   ├── __init__.py
│   │   ├── config.py              # 配置加载（环境变量）
│   │   └── constants.py          # 常量（默认值、限制）
│   │
│   ├── domain/                    # 【领域层】数据结构与契约
│   │   ├── __init__.py
│   │   ├── schemas.py             # 请求/响应 Pydantic 模型
│   │   ├── models.py              # 领域模型（如 ModelInfo）
│   │   └── interfaces.py          # 抽象接口（ImageGenerator 等）
│   │
│   ├── services/                  # 【服务层】业务逻辑
│   │   ├── __init__.py
│   │   ├── image_service.py       # 文生图业务编排
│   │   └── model_service.py       # 模型列表业务
│   │
│   └── infrastructure/            # 【基础设施层】外部依赖
│       ├── __init__.py
│       ├── dashscope/
│       │   ├── __init__.py
│       │   ├── client.py          # HTTP 客户端封装
│       │   └── adapter.py         # 实现 ImageGenerator 接口
│       └── data/
│           ├── __init__.py
│           └── model_repository.py  # 模型元数据（静态数据）
│
├── static/
│   ├── index.html
│   └── models.html
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest fixtures
│   └── api/
│       └── test_generate.py
│
├── docs/
├── requirements.txt
├── Dockerfile
├── .env.example
├── pyproject.toml                 # 可选：项目元数据、工具配置
└── README.md
```

---

## 四、模块职责与依赖关系

### 4.1 模块职责表

| 模块 | 职责 | 依赖 | 被依赖 |
|------|------|------|--------|
| **api/** | 接收 HTTP 请求、校验参数、调用 Service、返回响应 | core, domain, services | - |
| **core/** | 配置、常量，无业务逻辑 | - | api, services, infrastructure |
| **domain/** | 数据结构、接口定义，无外部依赖 | - | api, services, infrastructure |
| **services/** | 业务编排，调用 Infrastructure 完成业务 | domain, infrastructure(接口) | api |
| **infrastructure/** | 实现外部 API 调用、数据访问 | domain, core | services |

### 4.2 依赖关系图

```
                    main.py
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  api/v1/generate.py  │  api/v1/models.py                │
│  - 参数校验            │  - 无参数                        │
│  - 调用 ImageService  │  - 调用 ModelService             │
└───────────┬───────────┴────────────────┬─────────────────┘
            │                            │
            ▼                            ▼
┌───────────────────────┐    ┌───────────────────────────┐
│  services/            │    │  services/                │
│  image_service.py     │    │  model_service.py         │
│  - 校验 model 合法性   │    │  - 获取模型列表            │
│  - 调用 ImageGenerator│    │  - 调用 ModelRepository   │
└───────────┬───────────┘    └─────────────┬─────────────┘
            │                              │
            │  (依赖 domain.Interfaces)     │
            ▼                              ▼
┌───────────────────────┐    ┌───────────────────────────┐
│  infrastructure/       │    │  infrastructure/data/      │
│  dashscope/adapter.py  │    │  model_repository.py       │
│  - 实现 ImageGenerator │    │  - 返回静态模型数据          │
│  - 调用 DashScopeClient│    └───────────────────────────┘
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  infrastructure/       │
│  dashscope/client.py   │
│  - 纯 HTTP 调用        │
│  - 无业务逻辑          │
└───────────────────────┘
```

---

## 五、关键设计：接口与依赖注入

### 5.1 抽象接口（domain/interfaces.py）

```python
# 文生图能力抽象，便于替换实现（如 FLUX、Mock）
from abc import ABC, abstractmethod
from app.domain.schemas import GenerateInput, GenerateResult

class ImageGenerator(ABC):
    @abstractmethod
    def generate(self, input: GenerateInput) -> GenerateResult:
        pass
```

### 5.2 依赖注入（api/deps.py）

```python
# 通过 FastAPI Depends 注入，便于测试时替换
def get_config() -> Settings: ...
def get_image_generator() -> ImageGenerator: ...
def get_model_repository() -> ModelRepository: ...
def get_image_service(generator, config) -> ImageService: ...
def get_model_service(repo) -> ModelService: ...
```

### 5.3 低耦合收益

- **替换 DashScope**：实现新的 `ImageGenerator` 即可，Service 层无需改动
- **单元测试**：Mock `ImageGenerator`、`ModelRepository` 即可测试 Service
- **新增 FLUX**：新增 `FluxAdapter` 实现 `ImageGenerator`，Service 按 model 选择 adapter

---

## 六、各层代码规划

### 6.1 API 层（api/）

| 文件 | 职责 | 行数级 |
|------|------|--------|
| `deps.py` | 依赖注入工厂 | ~30 |
| `v1/router.py` | 聚合路由，挂载到 app | ~15 |
| `v1/generate.py` | 接收 GenerateRequest，调用 ImageService，返回 GenerateResponse | ~40 |
| `v1/models.py` | 调用 ModelService，返回模型列表（供首页下拉菜单选项） | ~15 |

**原则**：不包含 if/else 业务分支，只做「接收 → 调用 → 返回」。

---

### 6.2 核心层（core/）

| 文件 | 职责 |
|------|------|
| `config.py` | `Settings` 类，从环境变量加载，提供 `get_settings()` |
| `constants.py` | `DEFAULT_MODEL`、`MAX_PROMPT_LEN`、`DEFAULT_NEGATIVE_PROMPT` 等 |

---

### 6.3 领域层（domain/）

| 文件 | 职责 |
|------|------|
| `schemas.py` | `GenerateRequest`、`GenerateResponse`、`ModelInfo`、`ModelsResponse`、`ErrorResponse` |
| `models.py` | 领域值对象（若有） |
| `interfaces.py` | `ImageGenerator`、`ModelRepository` 抽象接口 |

---

### 6.4 服务层（services/）

| 文件 | 职责 |
|------|------|
| `image_service.py` | `ImageService.generate(input)`：校验 model、调用 ImageGenerator、封装结果 |
| `model_service.py` | `ModelService.list_models()`：调用 ModelRepository，过滤（如仅 unified） |

---

### 6.5 基础设施层（infrastructure/）

| 文件 | 职责 |
|------|------|
| `dashscope/client.py` | `DashScopeClient`：`post(url, payload)` 纯 HTTP，无业务语义 |
| `dashscope/adapter.py` | `DashScopeImageAdapter(ImageGenerator)`：构造 payload、解析响应 |
| `data/model_repository.py` | `ModelRepository`：返回 `list[ModelInfo]`，数据可来自 JSON/代码 |

---

## 七、数据流与调用链

### 7.1 生成图片

```
Client POST /api/v1/generate
  → api/v1/generate.generate_handler()
  → 校验 GenerateRequest (Pydantic)
  → image_service.generate(input)
      → 校验 model 在支持列表中
      → image_generator.generate(input)  # 注入的 DashScopeAdapter
          → dashscope_client.post(...)
          → 解析 JSON → GenerateResult
  → 封装 GenerateResponse
  → 返回 JSON
```

### 7.2 获取模型列表

```
Client GET /api/v1/models
  → api/v1/models.list_models_handler()
  → model_service.list_models()
      → model_repository.get_all()
  → 返回 ModelsResponse
```

---

## 八、扩展点（保持低耦合）

| 扩展需求 | 改动范围 | 说明 |
|----------|----------|------|
| 新增 FLUX 模型 | infrastructure/dashscope/ 或新建 flux/ | 新增 `FluxAdapter`，Service 按 model 选择 |
| 新增万相异步 | infrastructure/ 新增 wanx_async_client | 同上 |
| 模型数据改为 DB | infrastructure/data/model_repository.py | 实现从 DB 读取，接口不变 |
| 增加鉴权 | api/deps.py + 中间件 | 不影响 Service |
| 增加限流 | api 层中间件 | 不影响 Service |

---

## 九、与 PROJECT_PLAN / TODO 的对应

| 规划任务 | 对应文件 |
|----------|----------|
| config | core/config.py, core/constants.py |
| schemas、interfaces | domain/schemas.py, domain/interfaces.py |
| 文生图 API 调用 | infrastructure/dashscope/client.py, adapter.py |
| 业务编排 | services/image_service.py |
| 模型数据 | infrastructure/data/model_repository.py |
| 路由、依赖注入 | api/deps.py, api/v1/generate.py, api/v1/models.py |
| 应用入口 | main.py |

---

## 十、代码规范与边界

### 10.1 导入规则（避免循环依赖）

| 层 | 可导入 | 不可导入 |
|----|--------|----------|
| api | core, domain, services | infrastructure（直接） |
| services | domain, infrastructure（通过接口） | api |
| infrastructure | domain, core | services, api |
| domain | - | 所有其他层 |
| core | - | 所有其他层 |

### 10.2 文件命名

- 模块：小写 + 下划线（`image_service.py`）
- 类：大驼峰（`ImageService`、`GenerateRequest`）
- 接口：大驼峰，动词或能力名（`ImageGenerator`、`ModelRepository`）

### 10.3 模块边界检查

- `api/` 下不出现 `requests`、`httpx` 等 HTTP 客户端
- `services/` 下不出现 FastAPI 的 `Request`、`Response`
- `domain/` 下不出现 `os.getenv`、配置文件路径
- `infrastructure/` 不依赖 `services/`

---

## 十一、总结

| 原则 | 实现方式 |
|------|----------|
| **低耦合** | 分层、接口抽象、依赖注入、配置分离 |
| **高内聚** | 按职责分模块、API/Service/Infra 各司其职 |
| **可测试** | 接口可 Mock，各层可独立单测 |
| **可扩展** | 新增模型/数据源只需扩展 Infrastructure，不改 Service |
