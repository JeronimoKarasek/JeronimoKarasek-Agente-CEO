from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from .api.http import router as api_router
from .api.webhooks import router as hooks_router
from .api.metrics import router as metrics_router, requests_total
from .api.admin import router as admin_router
from .core.scheduler import start as start_scheduler
from .core.observability import setup_logging, set_corr_id, get_corr_id
from loguru import logger
import uuid

app = FastAPI(title="Agente-CEO Python")

# CORS for local dashboard file:// and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging()

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    corr = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    set_corr_id(corr)
    response: Response = await call_next(request)
    response.headers["X-Correlation-ID"] = get_corr_id() or corr
    return response

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    requests_total.inc()
    return await call_next(request)

app.include_router(api_router)
app.include_router(hooks_router)
app.include_router(metrics_router)
app.include_router(admin_router)

@app.get('/health')
async def health():
    return {'ok': True}

@app.on_event("startup")
async def _startup():
    await start_scheduler()
    logger.info({"event": "scheduler_started"})
