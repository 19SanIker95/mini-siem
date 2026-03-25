
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.event import EventIn, EventOut
from app.models.event import Event

router = APIRouter()

@router.post("/ingest", response_model=EventOut)
def ingest_event(payload: EventIn, db: Session = Depends(get_db)):
    ev = Event(**payload.model_dump())
    db.add(ev)
    db.flush()      # garante ID gerado antes de retornar
    db.refresh(ev)
    return ev
