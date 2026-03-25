
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, JSON, Index, text
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)          # windows/linux/firewall/app
    event_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)     # auth/process/network/...
    severity: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)

    host: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    user: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    ip: Mapped[str | None] = mapped_column(INET, nullable=True, index=True)

    message: Mapped[str] = mapped_column(String, nullable=False)

    raw: Mapped[dict] = mapped_column(JSON, nullable=False, server_default=text("'{}'::json"))

Index("ix_events_source_type_ts", Event.source, Event.event_type, Event.ts)
Index("ix_events_ip_ts", Event.ip, Event.ts)
