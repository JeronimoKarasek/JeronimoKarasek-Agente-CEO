from __future__ import annotations

import json
from loguru import logger
from typing import Any

from app.core.db import get_client
from app.services import products, creatives, publish, ads, analytics, supervisor


def run_task(task_type: str, payload: dict[str, Any], workspace_id: str, idempotency_key: str | None = None) -> dict:
    logger.info({"event": "worker_task_start", "type": task_type, "workspace_id": workspace_id})
    # Route to services
    if task_type == "run_scout":
        term = payload.get("search_term", "trending dropshipping product")
        return _await_sync(products.scout_once(search_term=term))
    if task_type == "run_creatives":
        return _await_sync(creatives.generate_for_product(payload["product_id"], variants=payload.get("variants", 5)))
    if task_type == "run_publish":
        return {"result": _await_sync(publish.queue_publications(payload["creative_ids"], platform=payload.get("platform", "tiktok")))}
    if task_type == "ads_launch":
        return {"result": _await_sync(ads.launch_campaign(payload["name"], payload.get("platform", "meta"), payload.get("daily_budget", 50.0)))}
    if task_type == "plan_daily":
        return _await_sync(supervisor.daily_plan())
    if task_type == "metrics_consolidate":
        return _await_sync(analytics.consolidate_daily_metrics(payload.get("date")))
    raise ValueError(f"Unknown task type: {task_type}")


def _await_sync(coro):
    # Simple helper to run async code when worker executed synchronously by RQ
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def poll_and_run_once() -> int:
    """DB-backed polling worker for fallback when Redis is unavailable."""
    client = get_client()
    # Find one queued task
    res = client.table("tasks").select("id,type,payload,workspace_id,idempotency_key").eq("status", "queued").order("scheduled_for").limit(1).execute()
    if not res.data:
        return 0
    task = res.data[0]
    client.table("tasks").update({"status": "running"}).eq("id", task["id"]).execute()
    try:
        payload = json.loads(task["payload"]) if isinstance(task["payload"], str) else task["payload"]
        result = run_task(task["type"], payload, task["workspace_id"], task.get("idempotency_key"))
        client.table("tasks").update({"status": "done", "result_json": json.dumps(result)}).eq("id", task["id"]).execute()
    except Exception as e:  # mark failed
        logger.error({"event": "worker_task_error", "error": str(e)})
        client.table("tasks").update({"status": "failed", "error": str(e)}).eq("id", task["id"]).execute()
    return 1

