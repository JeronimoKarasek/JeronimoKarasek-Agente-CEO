"""
Worker loop script for processing background tasks.
This script continuously polls for tasks and processes them.
"""
import time
from loguru import logger
from app.workers.worker import poll_and_run_once


def main():
    """Main worker loop."""
    logger.info("Worker started")
    
    while True:
        try:
            processed = poll_and_run_once()
            # Sleep longer if no tasks were processed to reduce CPU usage
            sleep_time = 2 if processed == 0 else 0.1
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            logger.info("Worker stopped by user")
            break
        except Exception as e:
            logger.error(f"Worker error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
