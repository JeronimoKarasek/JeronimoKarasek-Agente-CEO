from ..core.db import get_client

async def generate_for_product(product_id: str, variants: int = 5):
    # Placeholder: write creative rows to supabase
    rows = [{"product_id": product_id, "variant": i+1, "status": "queued"} for i in range(variants)]
    res = get_client().table("creatives").insert(rows).execute()
    return res.data
