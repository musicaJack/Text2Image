一、最终 MVP 技术方案（优化版）
模块	技术	作用
LLM	Qwen API	优化用户输入 prompt
图像生成	Wanx API	生成图片
服务框架	FastAPI	提供 API
部署	Docker	一键运行
前端	HTML + JS	简单 UI

核心原则：

不部署模型

全部调用云 API

代码最少

容易扩展

二、系统流程（完整）

推荐流程：

用户输入文本
      │
      ▼
FastAPI 接收请求
      │
      ▼
调用 Qwen API
（优化 prompt）
      │
      ▼
调用 Wanx text2image
      │
      ▼
获得图片URL
      │
      ▼
返回前端显示

优点：

稳定

成本低

实现简单

三、系统架构图
Browser
   │
   ▼
FastAPI server
   │
   ├── Qwen API
   │       │
   │       └── prompt优化
   │
   └── Wanx Image API
           │
           └── text2image
四、项目目录结构（推荐）

建议做成这样：

text2image-mvp
│
├── app
│   ├── main.py
│   ├── qwen.py
│   ├── image.py
│   └── config.py
│
├── static
│   └── index.html
│
├── requirements.txt
├── Dockerfile
└── README.md

解释：

文件	作用
main.py	FastAPI入口
qwen.py	调用Qwen
image.py	调用Wanx
index.html	前端
Dockerfile	部署
五、API设计
1️⃣ 生成图片

接口：

POST /generate

请求：

{
 "prompt": "cyberpunk city"
}

返回：

{
 "prompt":"ultra detailed cyberpunk city night...",
 "image":"https://img-url"
}
2️⃣ 健康检查
GET /health

返回：

ok

用于 Docker / k8s。

六、核心代码逻辑
1 Qwen prompt优化

qwen.py

import requests
import os

API_KEY = os.getenv("QWEN_API_KEY")

def optimize_prompt(text):

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    payload = {
        "model": "qwen-plus",
        "input": {
            "prompt": f"Write a detailed prompt for image generation: {text}"
        }
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)

    return r.json()["output"]["text"]
2 图像生成

image.py

import requests
import os

API_KEY = os.getenv("QWEN_API_KEY")

def generate_image(prompt):

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

    payload = {
        "model": "wanx-v1",
        "input": {
            "prompt": prompt
        }
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)

    return r.json()["output"]["results"][0]["url"]
3 FastAPI入口

main.py

from fastapi import FastAPI
from pydantic import BaseModel

from qwen import optimize_prompt
from image import generate_image

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
def generate(data: Prompt):

    optimized = optimize_prompt(data.prompt)

    image_url = generate_image(optimized)

    return {
        "prompt": optimized,
        "image": image_url
    }

@app.get("/health")
def health():
    return {"status":"ok"}
七、前端页面（极简）

index.html

input box
button
fetch /generate
show image

流程：

输入 prompt
点击生成
调用 API
显示图片
八、Docker 部署

Dockerfile

FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn requests

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]

构建：

docker build -t text2image .

运行：

docker run -p 8000:8000 \
-e QWEN_API_KEY=xxxxx \
text2image

访问：

http://localhost:8000
九、开发时间评估
步骤	时间
FastAPI接口	30分钟
Qwen调用	10分钟
Wanx调用	10分钟
HTML页面	20分钟
Docker部署	20分钟

总时间：

约2小时即可完成 MVP

十、这个架构未来如何扩展

你这个架构未来非常好扩展：

可以增加：

功能	实现
历史记录	SQLite
用户登录	JWT
图片存储	S3 / OSS
异步任务	Celery
队列	Redis

最终可以升级成：

Midjourney-like 网站

💡如果你愿意，我可以 直接帮你把这个 MVP 变成一个完整 GitHub 项目模板，包括：

README

Docker

FastAPI

HTML UI

.env

API调用封装

你只需要：

git clone
docker run

5分钟跑起来。