from typing import List
from ..core.db import get_client
from ..models.product import Product

async def scout_once(search_term: str = "trending dropshipping product"):
    # Placeholder: insert a dummy product row for testing
    data = {"title": f"Scouted: {search_term}", "status": "scouted"}
    res = get_client().table("products").insert(data).execute()
    return res.data

async def list_products() -> List[Product]:
    res = get_client().table("products").select("*").execute()
    return res.data or []
