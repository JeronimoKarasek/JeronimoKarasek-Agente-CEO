from __future__ import annotations

from .abstractions import AdsProvider, CampaignSpec, AdsetSpec, AdSpec
from loguru import logger


class MetaProvider(AdsProvider):
    async def create_campaign(self, spec: CampaignSpec) -> str:
        logger.info({"event": "meta_create_campaign", "name": spec.name, "budget": spec.daily_budget})
        return "meta_campaign_1"

    async def create_adset(self, spec: AdsetSpec) -> str:
        logger.info({"event": "meta_create_adset", "campaign_id": spec.campaign_id})
        return "meta_adset_1"

    async def create_ad(self, spec: AdSpec) -> str:
        logger.info({"event": "meta_create_ad", "adset_id": spec.adset_id, "creative": spec.creative_ref})
        return "meta_ad_1"

