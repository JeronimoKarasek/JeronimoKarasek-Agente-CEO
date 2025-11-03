from datetime import date
from ..core.db import get_client

async def consolidate_daily_metrics(day: date) -> dict[str, str | float]:
    # Placeholder: return simple aggregation from orders
    orders = get_client().table("orders").select("revenue,status").execute().data or []
    revenue = sum(float(o.get("revenue",0)) for o in orders if o.get("status") == "paid")
    return {"date": str(day), "revenue": revenue}
