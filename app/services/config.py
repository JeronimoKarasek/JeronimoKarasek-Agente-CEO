from __future__ import annotations

from functools import lru_cache
from ..core.db import get_client


@lru_cache(maxsize=128)
def get_flags(workspace_id: str = "default") -> dict:
    try:
        res = get_client().table("config").select("*").eq("workspace_id", workspace_id).limit(1).execute()
        if res.data:
            row = res.data[0]
            return {
                "AUTO_MODE": bool(row.get("auto_mode", True)),
                "APPROVAL_MODE": bool(row.get("approval_mode", False)),
                "DRY_RUN": bool(row.get("dry_run", False)),
                "TARGET_ROAS": float(row.get("target_roas", 1.5)),
            }
    except Exception:
        pass
    return {"AUTO_MODE": True, "APPROVAL_MODE": False, "DRY_RUN": False, "TARGET_ROAS": 1.5}

