from ..core.db import get_client
from .preflight import score_preflight
from ..core.idempotency import compute_idempotency_key

async def generate_for_product(product_id: str, variants: int = 5):
    # Placeholder generation with preflight scoring
    rows = []
    for i in range(variants):
        score = score_preflight(duration_s=25, hook_ms=1500, cta_present=True, readability=0.8)
        status = "approved" if score >= 0.6 else "rejected"
        rows.append({
            "product_id": product_id,
            "variant": i + 1,
            "status": status,
            "preflight_score": score,
            "idempotency_key": compute_idempotency_key("creative", "default", {"product_id": product_id, "variant": i+1}),
        })
    res = get_client().table("creatives").upsert(rows, on_conflict="idempotency_key").execute()
    return res.data
