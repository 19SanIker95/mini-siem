

import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET, TIMESTAMP

from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    ts: Mapped = mapped_column(TIMESTAMP(timezone=True), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    severity: Mapped[int] = mapped_column(Integer, nullable=False, default=1, index=True)

    host: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    user: Mapped[str | None] = mapped_column("user", String(255), nullable=True, index=True)  # coluna "user" no SQL
    ip: Mapped[str | None] = mapped_column(INET, nullable=True, index=True)

    message: Mapped[str] = mapped_column(Text, nullable=False)
    raw: Mapped[dict] = mapped_column(JSONB, nullable=False)

    created_at: Mapped = m

