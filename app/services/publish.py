from ..core.db import get_client
from ..core.idempotency import compute_idempotency_key
from loguru import logger

async def queue_publications(creative_ids: list[str], platform: str = "tiktok"):
    rows = [{
        "creative_id": cid,
        "platform": platform,
        "status": "queued",
        "idempotency_key": compute_idempotency_key("publication", "default", {"creative_id": cid, "platform": platform})
    } for cid in creative_ids]
    return get_client().table("publications").upsert(rows, on_conflict="idempotency_key").execute().data

async def process_publication_queue():
    # Placeholder: mark queued publications as published
    queued = get_client().table("publications").select("id,status,platform").eq("status","queued").execute().data or []
    if not queued:
        return {"updated": 0}
    # Prefer official APIs (not implemented), fallback to Playwright
    for item in queued:
        logger.info({"event": "publish_attempt", "id": item["id"], "platform": item.get("platform")})
    ids = [item["id"] for item in queued]
    updated = get_client().table("publications").update({"status":"published"}).in_("id", ids).execute().data
    return {"updated": len(updated or [])}
