import time
from typing import Dict, Tuple

# simple in-memory rate limiter (per-process)
_buckets: Dict[Tuple[str, str], Tuple[int, float]] = {}


def allow(key: str, route: str, limit: int = 60, window_s: int = 60) -> bool:
    now = time.time()
    k = (key, route)
    count, reset = _buckets.get(k, (0, now + window_s))
    if now > reset:
        count, reset = 0, now + window_s
    if count >= limit:
        _buckets[k] = (count, reset)
        return False
    _buckets[k] = (count + 1, reset)
    return True

