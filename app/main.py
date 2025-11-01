from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.http import router as api_router
from .api.webhooks import router as hooks_router
from .core.scheduler import start as start_scheduler
from loguru import logger

app = FastAPI(title="Agente-CEO Python")

# CORS for local dashboard file:// and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(hooks_router)

@app.get('/health')
async def health():
    return {'ok': True}

@app.on_event("startup")
async def _startup():
    await start_scheduler()
    logger.info("Scheduler started.")
