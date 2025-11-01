from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

from loguru import logger

try:
    import rq
    from redis import Redis
except Exception:  # pragma: no cover
    rq = None  # type: ignore
    Redis = None  # type: ignore

from .db import get_client


@dataclass
class Task:
    type: str
    payload: dict[str, Any]
    workspace_id: str
    idempotency_key: Optional[str] = None


class TaskQueue:
    def __init__(self) -> None:
        self._use_redis = False
        self._rq_queue: Optional["rq.Queue"] = None

        redis_url = os.getenv("REDIS_URL")
        if redis_url and rq is not None and Redis is not None:
            try:
                conn = Redis.from_url(redis_url)
                self._rq_queue = rq.Queue("agente_ceo", connection=conn)
                self._use_redis = True
                logger.info({"event": "queue_backend", "backend": "redis"})
            except Exception as e:  # fallback
                logger.warning({"event": "queue_redis_error", "error": str(e)})
                self._use_redis = False
        if not self._use_redis:
            logger.info({"event": "queue_backend", "backend": "db"})

    def enqueue(self, task: Task) -> str:
        if self._use_redis and self._rq_queue is not None:
            job = self._rq_queue.enqueue("app.workers.worker.run_task", task.type, task.payload, task.workspace_id, task.idempotency_key)
            return job.get_id()
        # DB-backed fallback
        client = get_client()
        data = {
            "type": task.type,
            "payload": json.dumps(task.payload),
            "workspace_id": task.workspace_id,
            "status": "queued",
            "idempotency_key": task.idempotency_key,
            "scheduled_for": datetime.now(timezone.utc).isoformat(),
        }
        res = client.table("tasks").insert(data).execute()
        tid = res.data[0]["id"] if res.data else ""
        return tid

    def count_queued(self) -> int:
        if self._use_redis and self._rq_queue is not None:
            try:
                return self._rq_queue.count
            except Exception:
                return 0
        try:
            client = get_client()
            r = client.table("tasks").select("id", count="exact").eq("status", "queued").execute()
            return int(r.count or 0)
        except Exception:
            return 0
