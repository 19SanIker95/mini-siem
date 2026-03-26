from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, IPvAnyAddress


class AlertOut(BaseModel):
    id: UUID
    rule_name: str
    severity: int
    ip: Optional[IPvAnyAddress] = None
    event_count: int
    window_start: datetime
    window_end: datetime
    created_at: datetime

    class Config:
        from_attributes = True