from __future__ import annotations

from datetime import date
from loguru import logger
from .config import settings
from .db import get_client


def check_budget_guardrails(daily: float, weekly: float) -> None:
    if daily > settings.SAFE_BUDGET_CAP_DAILY:
        logger.error({"event": "budget_cap_daily_exceeded", "value": daily})
        try:
            get_client().table("alerts").insert({"workspace_id": "default", "severity": "error", "code": "budget_daily_cap", "message": f"Daily {daily} > cap"}).execute()
        except Exception:
            pass
        raise ValueError("Daily budget exceeds guardrail cap")
    if weekly > settings.SAFE_BUDGET_CAP_WEEKLY:
        logger.error({"event": "budget_cap_weekly_exceeded", "value": weekly})
        try:
            get_client().table("alerts").insert({"workspace_id": "default", "severity": "error", "code": "budget_weekly_cap", "message": f"Weekly {weekly} > cap"}).execute()
        except Exception:
            pass
        raise ValueError("Weekly budget exceeds guardrail cap")


def should_scale_up(campaign_id: str, min_events: int = 30, target_roas: float = 1.5) -> bool:
    # Example: use daily_metrics aggregated by campaign for last 7 days
    client = get_client()
    # This assumes a metrics view exists; placeholder logic
    res = client.rpc("get_campaign_window_stats", {"campaign_id": campaign_id, "days": 7}).execute()
    data = (res.data or [{}])[0]
    events = int(data.get("events", 0))
    roas = float(data.get("roas", 0))
    logger.info({"event": "scale_evaluate", "events": events, "roas": roas})
    return events >= min_events and roas >= target_roas
