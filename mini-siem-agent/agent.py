import time
import socket
import yaml
import requests
import threading
from datetime import datetime, timezone
from collectors.linux_auth import linux_auth_collector
from collectors.windows_security import windows_failed_logon_collector
from collectors.linux_auth import start_linux_auth

CONFIG_FILE = "config.yaml"

host = socket.gethostname()

threading.Thread(
    target=start_linux_auth,
    args=(send_event, config["linux_auth"], host),
    daemon=True
).start()



def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def build_event(event_type, message, severity, source):
    return {
        "source": source,
        "event_type": event_type,
        "severity": severity,
        "message": message,
        "host": socket.gethostname(),
        "ts": datetime.now(timezone.utc).isoformat()
    }


def send_event(url, event):
    try:
        r = requests.post(url, json=event, timeout=10)
        r.raise_for_status()
        print(f"[OK] Sent event: {event['event_type']}")
    except Exception as e:
        print(f"[ERROR] Failed to send event: {e}")


def main():
    config = load_config()

    siem_url = config["siem_url"]
    source = config.get("source", "agent")
    interval = config.get("interval_seconds", 10)
    severity = config.get("severity_heartbeat", 1)

    # Evento de arranque
    startup_event = build_event(
        event_type="agent_start",
        message="Agent started successfully",
        severity=1,
        source=source,
    )
    send_event(siem_url, startup_event)

    # Loop principal (heartbeat)
    while True:
        heartbeat_event = build_event(
            event_type="agent_heartbeat",
            message="Agent heartbeat",
            severity=severity,
            source=source,
        )
        send_event(siem_url, heartbeat_event)
        time.sleep(interval)


if __name__ == "__main__":
    main()