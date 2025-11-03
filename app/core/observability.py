from __future__ import annotations

import json
from contextvars import ContextVar
from loguru import logger
from typing import Any
from .db import get_client

_corr_id: ContextVar[str | None] = ContextVar("corr_id", default=None)


def set_corr_id(value: str | None) -> None:
    _corr_id.set(value)


def get_corr_id() -> str | None:
    return _corr_id.get()


class JsonLogSink:
    def __call__(self, message: Any) -> None:
        record = message.record
        payload: dict[str, Any] = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "message": record["message"],
            "module": record["module"],
            "function": record["function"],
        }
        corr = get_corr_id()
        if corr:
            payload["correlation_id"] = corr
        # Merge extra dict if provided
        if record.get("extra"):
            payload.update({k: v for k, v in record["extra"].items() if k != "serialized"})
        print(json.dumps(payload, ensure_ascii=False))


def setup_logging() -> None:
    # Remove default sinks and add JSON sink
    logger.remove()
    logger.add(JsonLogSink())


def write_audit(workspace_id: str, action: str, context: dict[str, Any] | None = None) -> None:
    try:
        get_client().table("audit_log").insert({
            "workspace_id": workspace_id,
            "action": action,
            "context": context or {},
        }).execute()
    except Exception:
        # Avoid raising in audit path
        pass
