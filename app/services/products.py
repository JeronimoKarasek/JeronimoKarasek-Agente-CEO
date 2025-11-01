from typing import List
from ..core.db import get_client
from ..models.product import Product
from ..core.idempotency import compute_idempotency_key

async def scout_once(search_term: str = "trending dropshipping product"):
    # Placeholder: insert a dummy product row for testing
    idem = compute_idempotency_key("product", "default", {"title": search_term})
    data = {"title": f"Scouted: {search_term}", "status": "scouted", "idempotency_key": idem}
    res = get_client().table("products").upsert(data, on_conflict="idempotency_key").execute()
    return res.data

async def list_products() -> List[Product]:
    res = get_client().table("products").select("*").execute()
    return res.data or []
