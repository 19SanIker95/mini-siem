
from fastapi import APIRouter
from app.api.v1.endpoints import health, ingest, events

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(ingest.router, tags=["ingest"])
router.include_router(events.router, tags=["events"])
