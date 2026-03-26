from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.event import Event
from app.schemas.event import EventIn, EventOut

router = APIRouter()

@router.post("/ingest", response_model=EventOut)
def ingest_event(event_in: EventIn, db: Session = Depends(get_db)):
    event = Event(
        ts=event_in.ts,
        source=event_in.source,
        event_type=event_in.event_type,
        severity=event_in.severity,
        host=event_in.host,
        user=event_in.user,
        ip=event_in.ip,
        message=event_in.message,
        raw=event_in.raw,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event