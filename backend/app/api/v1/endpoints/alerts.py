from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertOut

router = APIRouter()

@router.post("/alerts/run", response_model=list[AlertOut])
def run_bruteforce_rule(db: Session = Depends(get_db)):
    """
    Regra: >=5 eventos de auth falhada (severity >=3) no último minuto por IP.
    """
    sql = text("""
        select
            ip,
            count(*) as cnt,
            min(ts) as window_start,
            max(ts) as window_end
        from public.events
        where event_type = 'authentication'
          and severity >= 3
          and ts >= now() - interval '1 minute'
          and ip is not null
        group by ip
        having count(*) >= 5
    """)

    rows = db.execute(sql).all()
    alerts: list[Alert] = []

    for ip, cnt, w_start, w_end in rows:
        alert = Alert(
            rule_name="bruteforce_authentication",
            severity=5,
            ip=ip,
            event_count=cnt,
            window_start=w_start,
            window_end=w_end,
        )
        db.add(alert)
        alerts.append(alert)

    if alerts:
        db.commit()
        for a in alerts:
            db.refresh(a)

    return alerts


@router.get("/alerts", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.created_at.desc()).all()

