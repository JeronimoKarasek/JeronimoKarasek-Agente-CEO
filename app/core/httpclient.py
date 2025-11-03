from __future__ import annotations

import time
from typing import Optional, Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError


class CircuitBreaker:
    def __init__(self, max_failures: int = 5, reset_after_s: int = 30) -> None:
        self.max_failures = max_failures
        self.reset_after_s = reset_after_s
        self.failures = 0
        self.open_until: Optional[float] = None

    def allow(self) -> bool:
        if self.open_until and time.time() < self.open_until:
            return False
        return True

    def record_success(self) -> None:
        self.failures = 0
        self.open_until = None

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.max_failures:
            self.open_until = time.time() + self.reset_after_s


class HttpClient:
    def __init__(self, timeout_s: float = 15.0) -> None:
        self._client = httpx.AsyncClient(timeout=timeout_s)
        self._cb = CircuitBreaker()

    async def close(self) -> None:
        await self._client.aclose()

    @retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=5), stop=stop_after_attempt(3))
    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        if not self._cb.allow():
            raise RuntimeError("circuit_open")
        try:
            resp = await self._client.request(method, url, **kwargs)
            if 500 <= resp.status_code < 600:
                raise httpx.HTTPError(f"server_error:{resp.status_code}")
            self._cb.record_success()
            return resp
        except Exception:
            self._cb.record_failure()
            raise

