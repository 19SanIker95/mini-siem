
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
import uuid

class EventIn(BaseModel):
    ts: datetime
    source: str = Field(..., max_length=50)
    event_type: str = Field(..., max_length=80)
    severity: int = Field(1, ge=0, le=10)

    host: Optional[str] = None
    user: Optional[str] = None
    ip: Optional[str] = None

    message: str
    raw: Dict[str, Any] = Field(default_factory=dict)

class EventOut(EventIn):
    id: uuid.UUID
