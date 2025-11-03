from fastapi import APIRouter, HTTPException
from ..services import products, creatives, publish, ads, analytics, supervisor
from datetime import date
from typing import List
from ..core.queue import TaskQueue, Task
from ..core.observability import get_corr_id
from ..core.ratelimit import allow
from loguru import logger

router = APIRouter(prefix="/api")
queue = TaskQueue()

@router.post("/run/scout")
async def run_scout(search_term: str = "trending dropshipping product", workspace_id: str = "default", async_mode: bool = True):
    if not allow(workspace_id, "run_scout", limit=30, window_s=60):
        return {"error": "rate_limited"}
    try:
        if async_mode:
            tid = queue.enqueue(Task(type="run_scout", payload={"search_term": search_term, "correlation_id": get_corr_id()}, workspace_id=workspace_id))
            return {"enqueued": True, "task_id": tid}
        return await products.scout_once(search_term=search_term)
    except Exception as e:
        logger.error({"event": "run_scout_error", "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run/creatives/{product_id}")
async def run_creatives(product_id: str, variants: int = 5, workspace_id: str = "default", async_mode: bool = True):
    if not allow(workspace_id, "run_creatives", limit=30, window_s=60):
        return {"error": "rate_limited"}
    try:
        if async_mode:
            tid = queue.enqueue(Task(type="run_creatives", payload={"product_id": product_id, "variants": variants}, workspace_id=workspace_id))
            return {"enqueued": True, "task_id": tid}
        return await creatives.generate_for_product(product_id, variants=variants)
    except Exception as e:
        logger.error({"event": "run_creatives_error", "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run/publish")
async def run_publish(creative_ids: List[str], platform: str = "tiktok", workspace_id: str = "default", async_mode: bool = True):
    if not allow(workspace_id, "run_publish", limit=60, window_s=60):
        return {"error": "rate_limited"}
    try:
        if async_mode:
            tid = queue.enqueue(Task(type="run_publish", payload={"creative_ids": creative_ids, "platform": platform}, workspace_id=workspace_id))
            return {"enqueued": True, "task_id": tid}
        return await publish.queue_publications(creative_ids, platform=platform)
    except Exception as e:
        logger.error({"event": "run_publish_error", "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ads/launch")
async def ads_launch(name: str, platform: str = "meta", daily_budget: float = 50.0, workspace_id: str = "default", async_mode: bool = True):
    if not allow(workspace_id, "ads_launch", limit=20, window_s=60):
        return {"error": "rate_limited"}
    try:
        if async_mode:
            tid = queue.enqueue(Task(type="ads_launch", payload={"name": name, "platform": platform, "daily_budget": daily_budget}, workspace_id=workspace_id))
            return {"enqueued": True, "task_id": tid}
        return await ads.launch_campaign(name=name, platform=platform, daily_budget=daily_budget)
    except Exception as e:
        logger.error({"event": "ads_launch_error", "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/summary")
async def metrics_summary():
    try:
        return await analytics.consolidate_daily_metrics(date.today())
    except Exception as e:
        logger.error({"event": "metrics_summary_error", "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run/plan/daily")
async def run_plan_daily(workspace_id: str = "default", async_mode: bool = True):
    if not allow(workspace_id, "plan_daily", limit=10, window_s=60):
        return {"error": "rate_limited"}
    try:
        if async_mode:
            tid = queue.enqueue(Task(type="plan_daily", payload={}, workspace_id=workspace_id))
            return {"enqueued": True, "task_id": tid}
        return await supervisor.daily_plan()
    except Exception as e:
        logger.error({"event": "plan_daily_error", "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))
