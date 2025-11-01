from datetime import date
from . import analytics

async def daily_plan():
    today = date.today()
    return await analytics.consolidate_daily_metrics(today)
