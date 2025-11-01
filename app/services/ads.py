from ..core.db import get_client

async def launch_campaign(name: str, platform: str = "meta", daily_budget: float = 50.0):
    row = {"name": name, "platform": platform, "daily_budget": daily_budget, "status": "draft"}
    return get_client().table("campaigns").insert(row).execute().data
