# Text2Image 开发 To-Do List

> 按架构分层开发，低耦合、高内聚。详见 `docs/ARCHITECTURE.md`。

---

## Phase 1：基础框架（MVP）✅

### 1.1 项目初始化 ✅
- [x] 创建目录结构（api/core/domain/services/infrastructure）
- [x] requirements.txt
- [x] .env.example

### 1.2 核心层 core/ ✅
- [x] config.py（Settings，环境变量）
- [x] constants.py（默认值、限制）

### 1.3 领域层 domain/ ✅
- [x] schemas.py（GenerateRequest、GenerateResponse、ModelInfo 等）
- [x] interfaces.py（ImageGenerator、ModelRepository 抽象）

### 1.4 基础设施层 infrastructure/ ✅
- [x] dashscope/client.py（HTTP 客户端）
- [x] dashscope/adapter.py（实现 ImageGenerator）
- [x] data/model_repository.py（模型元数据）

### 1.5 服务层 services/ ✅
- [x] image_service.py（业务编排）
- [x] model_service.py（模型列表）

### 1.6 API 层 api/ ✅
- [x] deps.py（依赖注入）
- [x] v1/generate.py（POST /api/v1/generate）
- [x] v1/models.py（GET /api/v1/models）
- [x] v1/router.py（路由聚合）

### 1.7 应用入口 ✅
- [x] main.py（挂载路由、/health）
- [x] index.html（首页）
- [x] models.html（模型介绍页）
- [x] Dockerfile、README.md

---

## Phase 2：模型介绍页 ✅

- [x] infrastructure/data/model_repository.py（模型元数据）
- [x] services/model_service.py
- [x] api/v1/models.py（GET /api/v1/models）
- [x] models.html（模型介绍页，动态加载）
- [x] 首页「模型介绍」入口

---

## Phase 3：体验优化

- [x] 前端模型下拉从 /api/v1/models 动态加载
- [ ] 加载状态、错误提示优化
- [ ] 根据模型调整 size 可选值（可选）

---

## Phase 4：扩展（可选）

- [ ] FLUX：infrastructure/flux/adapter.py
- [ ] 万相异步
- [ ] 图像持久化
- [ ] 历史记录
