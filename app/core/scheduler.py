from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

scheduler = AsyncIOScheduler()


async def start():
    try:
        scheduler.start()
        # Periodic DB-queue poller (fallback when Redis is not in use)
        try:
            from ..workers.worker import poll_and_run_once

            scheduler.add_job(poll_and_run_once, IntervalTrigger(seconds=5), id="db_queue_poller", replace_existing=True)
        except Exception as e:
            logger.warning({"event": "poller_setup_failed", "error": str(e)})

        # Refresh materialized views every 5 minutes
        scheduler.add_job(refresh_materialized_views, IntervalTrigger(minutes=5), id="refresh_mviews", replace_existing=True)
        logger.info("APScheduler started")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")


def refresh_materialized_views():
    try:
        from .db import get_client

        client = get_client()
        client.rpc("exec_sql", {"sql": "refresh materialized view concurrently mv_daily_roas;"}).execute()
        client.rpc("exec_sql", {"sql": "refresh materialized view concurrently mv_campaign_cac;"}).execute()
        logger.info({"event": "mviews_refreshed"})
    except Exception as e:
        logger.warning({"event": "mviews_refresh_failed", "error": str(e)})
