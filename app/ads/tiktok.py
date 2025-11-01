from __future__ import annotations

from .abstractions import AdsProvider, CampaignSpec, AdsetSpec, AdSpec
from loguru import logger


class TiktokProvider(AdsProvider):
    async def create_campaign(self, spec: CampaignSpec) -> str:
        logger.info({"event": "tiktok_create_campaign", "name": spec.name, "budget": spec.daily_budget})
        return "tt_campaign_1"

    async def create_adset(self, spec: AdsetSpec) -> str:
        logger.info({"event": "tiktok_create_adset", "campaign_id": spec.campaign_id})
        return "tt_adset_1"

    async def create_ad(self, spec: AdSpec) -> str:
        logger.info({"event": "tiktok_create_ad", "adset_id": spec.adset_id, "creative": spec.creative_ref})
        return "tt_ad_1"

