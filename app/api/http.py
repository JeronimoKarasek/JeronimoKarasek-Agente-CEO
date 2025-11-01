from fastapi import APIRouter
from ..services import products, creatives, publish, ads, analytics, supervisor
from datetime import date
from typing import List

router = APIRouter(prefix="/api")

@router.post("/run/scout")
async def run_scout(search_term: str = "trending dropshipping product"):
    return await products.scout_once(search_term=search_term)

@router.post("/run/creatives/{product_id}")
async def run_creatives(product_id: str, variants: int = 5):
    return await creatives.generate_for_product(product_id, variants=variants)

@router.post("/run/publish")
async def run_publish(creative_ids: List[str], platform: str = "tiktok"):
    return await publish.queue_publications(creative_ids, platform=platform)

@router.post("/ads/launch")
async def ads_launch(name: str, platform: str = "meta", daily_budget: float = 50.0):
    return await ads.launch_campaign(name=name, platform=platform, daily_budget=daily_budget)

@router.get("/metrics/summary")
async def metrics_summary():
    return await analytics.consolidate_daily_metrics(date.today())

@router.post("/run/plan/daily")
async def run_plan_daily():
    return await supervisor.daily_plan()
