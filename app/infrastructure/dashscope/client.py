"""DashScope HTTP 客户端：纯 HTTP 调用，无业务语义."""

from typing import Optional

import requests

from app.core.config import get_settings


class DashScopeClient:
    """DashScope API HTTP 客户端."""

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        settings = get_settings()
        self.base_url = (base_url or settings.dashscope_base_url).rstrip("/")
        self.api_key = api_key or settings.dashscope_api_key
        self.timeout = settings.request_timeout

    def post(self, path: str, payload: dict) -> dict:
        """发送 POST 请求."""
        url = f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        return resp.json()
