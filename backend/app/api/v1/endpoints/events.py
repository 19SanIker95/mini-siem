from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.event import Event            # ✅ IMPORTA O ORM CERTO
from app.schemas.event import EventOut        # ✅ usa o teu schema existente
from app.schemas.stats import EventsStatsOut, RangeOut

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



@router.get("/events/stats", response_model=EventsStatsOut)
def events_stats(
    db: Session = Depends(get_db),
    # Filtros opcionais (se não enviares nada, usa últimos 24h)
    start: datetime | None = None,
    end: datetime | None = None,
    since_minutes: int = Query(default=1440, ge=1, le=525600),  # 24h por defeito
):
    now = datetime.now(timezone.utc)

    if end is None:
        end = now
    if start is None:
        start = end - timedelta(minutes=since_minutes)

    # Total
    total = db.execute(
        select(func.count()).select_from(Event).where(Event.ts >= start, Event.ts <= end)
    ).scalar_one()

    # By severity
    sev_rows = db.execute(
        select(Event.severity, func.count())
        .where(Event.ts >= start, Event.ts <= end)
        .group_by(Event.severity)
        .order_by(Event.severity)
    ).all()
    by_severity = {str(sev): cnt for sev, cnt in sev_rows}

    # By source
    src_rows = db.execute(
        select(Event.source, func.count())
        .where(Event.ts >= start, Event.ts <= end)
        .group_by(Event.source)
        .order_by(Event.source)
    ).all()
    by_source = {str(src): cnt for src, cnt in src_rows}

    # By event_type
    type_rows = db.execute(
        select(Event.event_type, func.count())
        .where(Event.ts >= start, Event.ts <= end)
        .group_by(Event.event_type)
        .order_by(Event.event_type)
    ).all()
    by_event_type = {str(et): cnt for et, cnt in type_rows}

    return EventsStatsOut(
        range=RangeOut(start=start, end=end),
        total=total,
        by_severity=by_severity,
        by_source=by_source,
        by_event_type=by_event_type,
    )