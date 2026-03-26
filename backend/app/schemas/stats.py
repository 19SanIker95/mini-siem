from datetime import datetime
from pydantic import BaseModel
from typing import Dict

class RangeOut(BaseModel):
    start: datetime
    end: datetime

class EventsStatsOut(BaseModel):
    range: RangeOut
    total: int
    by_severity: Dict[str, int]
    by_source: Dict[str, int]
    by_event_type: Dict[str, int]