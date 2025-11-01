import hmac
import hashlib
import time
from typing import Optional

from .config import settings
from .db import get_client


def verify_hmac_signature(body: bytes, signature: str) -> bool:
    secret = (settings.SUPABASE_SERVICE_KEY or "").encode()
    # Prefer a dedicated WEBHOOK_SECRET if available
    # Fallback to service key only for demo/dev
    webhook_secret = getattr(settings, "WEBHOOK_SECRET", None)
    if webhook_secret:
        secret = webhook_secret.encode()
    digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
    # Timing-safe compare
    return hmac.compare_digest(digest, signature)


def is_replay(event_id: str, window_seconds: int = 600) -> bool:
    client = get_client()
    now = int(time.time())
    res = client.table("webhook_events").select("event_id,received_at").eq("event_id", event_id).execute()
    if res.data:
        # if received within window, it's a replay
        try:
            ts = int(res.data[0].get("received_at", now))
        except Exception:
            ts = now
        return now - ts < window_seconds
    client.table("webhook_events").insert({"event_id": event_id, "received_at": now}).execute()
    return False

