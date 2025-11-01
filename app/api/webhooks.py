from fastapi import APIRouter, Request
from ..services import crm

router = APIRouter(prefix="/api/webhooks")

@router.post("/checkout")
async def checkout_hook(req: Request):
    body = await req.json()
    return await crm.process_checkout_webhook(body)
