# 阿里云图像模型调研：各模型特点与 API 可选用性

> 基于截图中的模型列表，结合官方 API 文档，梳理各模型特点及是否可做成可选模型。

---

## 一、模型分类总览

| 类别 | 模型 | 用途 | API 可选用 | 说明 |
|------|------|------|------------|------|
| **Qwen 文生图** | Qwen-Image-2.0、2.0-Pro、Max、Plus | 纯文生图 | ✅ 是 | 统一 multimodal-generation 接口 |
| **Qwen 图编辑** | Qwen-Image-Edit-Max、Edit-Plus | 图+文→图 | ⚠️ 部分 | 需传入图片，非纯文生图 |
| **万相** | Wan-T2I（wan2.6-t2i 等） | 纯文生图 | ✅ 是 | 2.6 同步，2.5 及以下异步 |
| **Z-Image** | Z-Image-Turbo | 纯文生图 | ✅ 是 | 轻量快速，统一接口 |
| **FLUX** | flux-schnell、flux-dev、flux-merged | 纯文生图 | ✅ 是 | 不同 API 端点，需单独适配 |
| **AI 试衣** | AI试衣-Plus、基础版 | 试衣专用 | ❌ 否 | 需模特图+服饰图，场景不同 |

---

## 二、各模型特点详解

### 2.1 Qwen-Image 文生图系列

| 模型 | 特点 | 输出规格 | 接口 |
|------|------|----------|------|
| **qwen-image-2.0-pro** | 文字渲染、真实质感、语义遵循更强 | 512²~2048²，1~6 张 | 同步 |
| **qwen-image-2.0** | 加速版，效果与速度平衡 | 同上 | 同步 |
| **qwen-image-max** | 真实感、自然度更强，AI 痕迹更低 | 固定 1 张，固定比例 | 同步 |
| **qwen-image-plus** | 艺术风格多样、文字渲染好 | 固定 1 张 | 同步/异步 |

**API 端点**：`POST .../multimodal-generation/generation`  
**请求格式**：`input.messages` 中仅 `text`，无图片。

---

### 2.2 Qwen-Image-Edit 图像编辑系列

| 模型 | 特点 | 输入要求 | 输出 |
|------|------|----------|------|
| **qwen-image-2.0-pro** | 生成+编辑合一 | 图+文 或 多图+文 | 1~6 张 |
| **qwen-image-2.0** | 同上，加速版 | 同上 | 同上 |
| **qwen-image-edit-max** | 工业设计、几何推理、角色一致性 | 图+文 | 1~6 张 |
| **qwen-image-edit-plus** | 多图输出、自定义分辨率 | 图+文 | 1~6 张 |
| **qwen-image-edit** | 单图编辑、多图融合 | 图+文 | 固定 1 张 |

**API 端点**：与文生图相同 `multimodal-generation/generation`  
**请求格式**：`input.messages[0].content` 需包含 `image`（URL）+ `text`。

**结论**：Edit 系列需要图片输入，不适合「纯文生图」场景；若产品支持「图编辑」功能，可单独入口、单独参数。

---

### 2.3 万相 Wan-T2I 系列

| 模型 | 特点 | 接口类型 | 分辨率 |
|------|------|----------|--------|
| **wan2.6-t2i** | 最新，自由尺寸 | 同步 | 1280²~1440²，宽高比 1:4~4:1 |
| **wan2.5-t2i-preview** | 预览版，支持超长图 | 异步 | 自由尺寸 |
| **wan2.2-t2i-flash** | 极速，速度提升约 50% | 异步 | 512~1440 |
| **wan2.2-t2i-plus** | 专业版，细节更好 | 异步 | 同上 |
| **wanx2.1-t2i-turbo** | 2.1 极速版 | 异步 | - |
| **wanx2.1-t2i-plus** | 2.1 专业版 | 异步 | - |
| **wanx2.0-t2i-turbo** | 2.0 极速版 | 异步 | - |

**API 端点**：
- wan2.6：`multimodal-generation/generation`（同步）
- 2.5 及以下：`text2image/image-synthesis`（异步，需轮询 task_id）

**请求格式**：wan2.6 与 Qwen-Image 类似，`messages` + `text`。

---

### 2.4 Z-Image-Turbo

| 项目 | 说明 |
|------|------|
| **特点** | 轻量、快速，支持中英文字渲染 |
| **分辨率** | 512²~2048²，推荐 1024²~1536² |
| **输出** | 固定 1 张 |
| **prompt_extend** | 可选，开启会返回优化 prompt 和推理过程，但增加耗时和费用 |

**API 端点**：`multimodal-generation/generation`  
**请求格式**：与 Qwen-Image 相同。

---

### 2.5 FLUX 系列（阿里直供）

| 模型 | 特点 |
|------|------|
| **flux-schnell** | 少步模型，速度快，质量高 |
| **flux-dev** | 非商业开源，质量接近专业版 |
| **flux-merged** | 推荐，结合 dev 深度与 schnell 速度 |

**限制**：
- 仅北京地域
- 免费体验，额度用完后不可付费续用
- 需单独申请审核

**API 端点**：`text2image/image-synthesis`（**与 Qwen/万相不同**）  
**调用方式**：**异步**，需 `X-DashScope-Async: enable`  
**请求格式**：`input.prompt`，无 `messages`。

---

### 2.6 AI 试衣

| 模型 | 说明 |
|------|------|
| **aitryon** | 基础版，快速试衣 |
| **aitryon-plus** | 清晰度、纹理、logo 还原更好，耗时更长 |

**输入**：模特图 + 服饰图，非纯文本。  
**结论**：与文生图场景不同，不适合作为「文生图可选模型」。

---

## 三、API 统一性分析

### 3.1 可统一调用的模型（同一端点、同一格式）

以下模型均使用：

- 端点：`POST .../multimodal-generation/generation`
- 格式：`input.messages` + `content[0].text`

| 模型名 | 说明 |
|--------|------|
| qwen-image-2.0-pro | Qwen 文生图 |
| qwen-image-2.0 | Qwen 文生图 |
| qwen-image-max | Qwen 文生图 |
| qwen-image-plus | Qwen 文生图 |
| qwen-image | Qwen 文生图 |
| z-image-turbo | Z-Image |
| wan2.6-t2i | 万相 2.6 |

**实现方式**：首页通过**下拉菜单**供用户选择模型，前端将选中项作为 `model` 参数传给后端，后端透传给 API 即可切换。

### 3.2 需单独适配的模型

| 模型 | 原因 |
|------|------|
| **FLUX 系列** | 不同端点（image-synthesis）、不同格式（input.prompt）、异步调用 |
| **万相 2.5 及以下** | 异步接口，需创建任务 + 轮询 task_id |

### 3.3 不适合纯文生图可选

| 模型 | 原因 |
|------|------|
| Qwen-Image-Edit 系列 | 必须传入图片 |
| AI 试衣 | 需模特图 + 服饰图 |

---

## 四、实现「多模型可选」的建议

### 4.1 方案 A：仅支持统一接口模型（推荐 MVP）

支持模型：`qwen-image-2.0-pro`、`qwen-image-2.0`、`qwen-image-max`、`qwen-image-plus`、`z-image-turbo`、`wan2.6-t2i`。

**实现**：
- 请求体增加 `model` 字段，默认如 `qwen-image-2.0-pro`
- 后端将 `model` 透传给 API，其余参数不变

**优点**：实现简单，无需分支逻辑。

### 4.2 方案 B：支持统一接口 + FLUX

在方案 A 基础上增加 FLUX 分支：

- 若 `model` 为 `flux-schnell` / `flux-dev` / `flux-merged`：
  - 调用 `text2image/image-synthesis`
  - 使用 `input.prompt` 格式
  - 异步：提交任务 → 轮询 `task_id` → 返回结果

**实现**：根据 `model` 选择不同调用路径和参数构造。

### 4.3 方案 C：支持统一接口 + FLUX + 万相异步

再增加万相 2.5 及以下模型的异步调用，逻辑与 FLUX 类似，但端点与参数需按万相文档实现。

---

## 五、推荐模型配置示例

```python
# 可选的文生图模型配置
T2I_MODELS = {
    # 统一 multimodal-generation 接口
    "unified": [
        {"id": "qwen-image-2.0-pro", "name": "Qwen-Image-2.0-Pro", "desc": "文字渲染、真实质感更强"},
        {"id": "qwen-image-2.0", "name": "Qwen-Image-2.0", "desc": "加速版，效果与速度平衡"},
        {"id": "qwen-image-max", "name": "Qwen-Image-Max", "desc": "真实感、自然度更强"},
        {"id": "qwen-image-plus", "name": "Qwen-Image-Plus", "desc": "艺术风格多样、文字渲染好"},
        {"id": "z-image-turbo", "name": "Z-Image-Turbo", "desc": "轻量快速，中英文字渲染"},
        {"id": "wan2.6-t2i", "name": "万相2.6", "desc": "万相最新，自由尺寸"},
    ],
    # 需单独适配（FLUX）
    "flux": [
        {"id": "flux-merged", "name": "FLUX-Merged", "desc": "推荐，质量与速度兼顾"},
        {"id": "flux-schnell", "name": "FLUX-Schnell", "desc": "少步快速"},
        {"id": "flux-dev", "name": "FLUX-Dev", "desc": "高质量，非商业"},
    ],
}
```

---

## 六、总结

| 问题 | 结论 |
|------|------|
| 截图中的模型能否都做成可选？ | **纯文生图**：Qwen、万相、Z-Image、FLUX 可以；**Edit 系列、AI 试衣**不适合纯文生图 |
| 实现难度 | 统一接口模型：仅改 `model` 即可；FLUX、万相异步需单独分支 |
| 推荐实现顺序 | 1）先支持 6 个统一接口模型；2）再按需支持 FLUX |
