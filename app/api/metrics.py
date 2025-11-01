from fastapi import APIRouter, Response
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest, Counter, Gauge

router = APIRouter()

_registry = CollectorRegistry()
requests_total = Counter("app_requests_total", "Total HTTP requests", registry=_registry)
queue_size = Gauge("app_queue_size", "Current queued tasks", registry=_registry)


@router.get("/metrics")
async def metrics() -> Response:
    # Values can be updated by services; keep basic output for now
    data = generate_latest(_registry)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

