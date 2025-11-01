from ..core.db import get_client

async def queue_publications(creative_ids: list[str], platform: str = "tiktok"):
    rows = [{"creative_id": cid, "platform": platform, "status": "queued"} for cid in creative_ids]
    return get_client().table("publications").insert(rows).execute().data

async def process_publication_queue():
    # Placeholder: mark queued publications as published
    queued = get_client().table("publications").select("id,status").eq("status","queued").execute().data or []
    if not queued:
        return {"updated": 0}
    ids = [q["id"] for q in queued]
    updated = get_client().table("publications").update({"status":"published"}).in_("id", ids).execute().data
    return {"updated": len(updated or [])}
