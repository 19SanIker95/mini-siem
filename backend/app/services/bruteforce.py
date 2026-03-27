from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.event import Event
from app.models.alert import Alert

WINDOW_SECONDS = 60
MAX_ATTEMPTS = 5


def detect_bruteforce(db: Session):
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(seconds=WINDOW_SECONDS)

    events = (
        db.query(Event)
        .filter(
            Event.event_type == "authentication",
            Event.ts >= window_start
        )
        .all()
    )

    buckets = {}

    for e in events:
        key = (e.ip, e.host)
        buckets.setdefault(key, []).append(e)

    for (ip, host), attempts in buckets.items():
        if ip is None:
            continue

        if len(attempts) >= MAX_ATTEMPTS:
            already = (
                db.query(Alert)
                .filter(
                    Alert.type == "bruteforce",
                    Alert.ip == ip,
                    Alert.host == host,
                    Alert.created_at >= window_start
                )
                .first()
            )

            if already:
                continue

            alert = Alert(
                type="bruteforce",
                severity=5,
                title="Possible brute force detected",
                description=(
                    f"{len(attempts)} failed login attempts from {ip} "
                    f"against {host} in {WINDOW_SECONDS}s"
                ),
                ip=ip,
                host=host,
                created_at=now
            )

            db.add(alert)
            db.commit()