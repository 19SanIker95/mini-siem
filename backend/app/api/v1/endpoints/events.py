from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.event import Event            # ✅ IMPORTA O ORM CERTO
from app.schemas.event import EventOut        # ✅ usa o teu schema existente

router = APIRouter()

@router.get("/events", response_model=list[EventOut])
def list_events(
    db: Session = Depends(get_db),

    source: Optional[str] = None,
    event_type: Optional[str] = None,
    host: Optional[str] = None,
    user: Optional[str] = None,
    ip: Optional[str] = None,

    min_severity: Optional[int] = Query(default=None, ge=0, le=10),
    max_severity: Optional[int] = Query(default=None, ge=0, le=10),

    start: Optional[datetime] = None,
    end: Optional[datetime] = None,

    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    stmt = select(Event)

    if source:
        stmt = stmt.where(Event.source == source)
    if event_type:
        stmt = stmt.where(Event.event_type == event_type)
    if host:
        stmt = stmt.where(Event.host == host)
    if user:
        stmt = stmt.where(Event.user == user)
    if ip:
        stmt = stmt.where(Event.ip == ip)

    if min_severity is not None:
        stmt = stmt.where(Event.severity >= min_severity)
    if max_severity is not None:
        stmt = stmt.where(Event.severity <= max_severity)

    if start:
        stmt = stmt.where(Event.ts >= start)
    if end:
        stmt = stmt.where(Event.ts <= end)

    stmt = stmt.order_by(desc(Event.ts)).offset(offset).limit(limit)

    return db.execute(stmt).scalars().all()