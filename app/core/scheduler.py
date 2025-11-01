from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

scheduler = AsyncIOScheduler()

async def start():
    try:
        scheduler.start()
        logger.info("APScheduler started")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
