
from fastapi import APIRouter
from app.api.v1.endpoints import health, ingest, events, alerts

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(ingest.router, tags=["ingest"])
router.include_router(events.router, tags=["events"])
router.include_router(alerts.router, tags=["alerts"])
