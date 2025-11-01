from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Optional, Dict, Any


@dataclass
class CampaignSpec:
    name: str
    daily_budget: float
    objective: Optional[str] = None


@dataclass
class AdsetSpec:
    campaign_id: str
    name: str
    bid_strategy: Optional[str] = None
    targeting_json: Optional[Dict[str, Any]] = None


@dataclass
class AdSpec:
    adset_id: str
    name: str
    creative_ref: str


class AdsProvider(Protocol):
    async def create_campaign(self, spec: CampaignSpec) -> str: ...
    async def create_adset(self, spec: AdsetSpec) -> str: ...
    async def create_ad(self, spec: AdSpec) -> str: ...

