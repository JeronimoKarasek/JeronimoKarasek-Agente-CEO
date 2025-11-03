from ..core.db import get_client

async def process_checkout_webhook(body: dict) -> list[dict]:
    # Minimal example: store order
    order = {
        "external_id": body.get("id"),
        "status": body.get("status","paid"),
        "revenue": float(body.get("amount", 0)),
    }
    return get_client().table("orders").insert(order).execute().data
