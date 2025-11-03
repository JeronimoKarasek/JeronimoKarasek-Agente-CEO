from ..core.db import get_client
from ..core.guardrails import check_budget_guardrails
from ..ads.meta import MetaProvider
from ..ads.tiktok import TiktokProvider
from ..ads.abstractions import CampaignSpec
from ..core.observability import write_audit
from ..core.idempotency import compute_idempotency_key

async def launch_campaign(name: str, platform: str = "meta", daily_budget: float = 50.0) -> list[dict]:
    check_budget_guardrails(daily=daily_budget, weekly=daily_budget * 7)
    provider = MetaProvider() if platform == "meta" else TiktokProvider()
    cid = await provider.create_campaign(CampaignSpec(name=name, daily_budget=daily_budget))
    row = {"name": name, "platform": platform, "external_id": cid, "daily_budget": daily_budget, "status": "draft", "idempotency_key": compute_idempotency_key("campaign", "default", {"name": name, "platform": platform})}
    data = get_client().table("campaigns").upsert(row, on_conflict="idempotency_key").execute().data
    write_audit("default", "campaign_created", {"platform": platform, "external_id": cid})
    return data
