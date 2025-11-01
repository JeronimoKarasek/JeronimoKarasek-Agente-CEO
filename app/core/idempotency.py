import hashlib
import json
from typing import Any


def compute_idempotency_key(prefix: str, workspace_id: str, payload: dict[str, Any]) -> str:
    base = {"w": workspace_id, "p": payload}
    s = json.dumps(base, sort_keys=True, separators=(",", ":"))
    return f"{prefix}_" + hashlib.sha256(s.encode()).hexdigest()[:32]

