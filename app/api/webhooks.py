from fastapi import APIRouter, Request, Header, HTTPException
from ..services import crm
from ..core.security import verify_hmac_signature, is_replay

router = APIRouter(prefix="/api/webhooks")

@router.post("/checkout")
async def checkout_hook(req: Request, x_signature: str | None = Header(default=None), x_event_id: str | None = Header(default=None)):
    raw = await req.body()
    if not x_signature or not verify_hmac_signature(raw, x_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    if x_event_id and is_replay(x_event_id):
        raise HTTPException(status_code=409, detail="Replay detected")
    body = await req.json()
    return await crm.process_checkout_webhook(body)
