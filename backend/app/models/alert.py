
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, func
from sqlalchemy.dialects.postgresql import UUID, INET, TIMESTAMP

from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )

    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[int] = mapped_column(Integer, nullable=False)

    ip: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    event_count: Mapped[int] = mapped_column(Integer, nullable=False)

    window_start: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    window_end: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
