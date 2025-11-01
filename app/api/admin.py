from fastapi import APIRouter
from ..core.queue import TaskQueue
from ..core.db import get_client
from ..services.config import get_flags

router = APIRouter(prefix="/api/admin")
queue = TaskQueue()


@router.get("/queue")
async def get_queue():
    return {"queued": queue.count_queued()}


@router.get("/alerts")
async def get_alerts(workspace_id: str = "default"):
    res = get_client().table("alerts").select("*").eq("workspace_id", workspace_id).order("created_at", desc=True).limit(50).execute()
    return res.data or []


@router.get("/audit")
async def get_audit(workspace_id: str = "default"):
    res = get_client().table("audit_log").select("*").eq("workspace_id", workspace_id).order("created_at", desc=True).limit(100).execute()
    return res.data or []


@router.get("/config")
async def read_config(workspace_id: str = "default"):
    return get_flags(workspace_id)


@router.post("/config")
async def write_config(workspace_id: str = "default", auto_mode: bool | None = None, approval_mode: bool | None = None, dry_run: bool | None = None, target_roas: float | None = None):
    values = {}
    if auto_mode is not None:
        values["auto_mode"] = auto_mode
    if approval_mode is not None:
        values["approval_mode"] = approval_mode
    if dry_run is not None:
        values["dry_run"] = dry_run
    if target_roas is not None:
        values["target_roas"] = target_roas
    if not values:
        return {"ok": True}
    get_client().table("config").upsert({"workspace_id": workspace_id, **values}).execute()
    return {"ok": True}
