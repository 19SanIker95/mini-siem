import json
import random
import argparse
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ----------------------------
# Helpers
# ----------------------------
def iso_utc(dt: datetime) -> str:
    """Return ISO-8601 string in UTC with 'Z'."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def post_json(url: str, payload: dict, timeout: int = 10) -> tuple[int, str]:
    """POST JSON using only stdlib."""
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url=url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return e.code, body
    except URLError as e:
        return 0, f"URLError: {e}"


# ----------------------------
# Event generators
# ----------------------------
USERS = ["tiago", "ana", "joao", "maria", "rui", "sofia"]
HOSTS = ["server-01", "server-02", "workstation-07", "workstation-12", "vpn-gw-01"]
PROGRAMS = {
    "linux": ["sshd", "sudo", "cron", "nginx"],
    "windows": ["Security", "Sysmon", "WinRM"],
    "app": ["auth-service", "payments-api", "gateway"],
}

def gen_ip(base: str, n: int) -> str:
    # base like "192.168.1." -> produce "192.168.1.10" etc.
    return f"{base}{n}"


def make_auth_event(ts: datetime, source: str, ip: str, user: str, host: str, success: bool) -> dict:
    # severity convention (example):
    # - success: 1
    # - fail: 3
    sev = 1 if success else 3
    msg = "Login successful" if success else "Failed login attempt"
    reason = "ok" if success else random.choice(["invalid password", "user not found", "account locked"])
    program = random.choice(PROGRAMS.get(source, ["auth"]))
    raw = {
        "program": program,
        "reason": reason,
        "success": success,
        "method": random.choice(["password", "ssh-key", "mfa"]),
    }
    return {
        "ts": iso_utc(ts),
        "source": source,
        "event_type": "authentication",
        "severity": sev,
        "host": host,
        "user": user,
        "ip": ip,
        "message": msg,
        "raw": raw,
    }


def make_network_event(ts: datetime, source: str, ip: str, host: str) -> dict:
    sev = random.choice([1, 2, 2, 3])  # bias low/medium
    dst_port = random.choice([22, 80, 443, 3389, 445, 8080, 8443])
    action = random.choice(["allowed", "blocked"])
    msg = f"Network connection {action} to port {dst_port}"
    raw = {
        "dst_port": dst_port,
        "action": action,
        "proto": random.choice(["tcp", "udp"]),
        "bytes": random.randint(200, 20000),
    }
    return {
        "ts": iso_utc(ts),
        "source": source,
        "event_type": "network",
        "severity": sev,
        "host": host,
        "user": None,
        "ip": ip,
        "message": msg,
        "raw": raw,
    }


def make_process_event(ts: datetime, source: str, host: str, user: str) -> dict:
    sev = random.choice([1, 1, 2, 3])
    proc = random.choice(["bash", "powershell", "python", "cmd", "curl", "wmic"])
    suspicious = proc in ["powershell", "wmic"] and random.random() < 0.25
    msg = f"Process started: {proc}"
    raw = {
        "process": proc,
        "pid": random.randint(100, 9999),
        "parent": random.choice(["system", "explorer", "sshd", "cron"]),
        "suspicious": suspicious,
    }
    if suspicious:
        sev = 4
        msg = f"Suspicious process started: {proc}"
    return {
        "ts": iso_utc(ts),
        "source": source,
        "event_type": "process",
        "severity": sev,
        "host": host,
        "user": user,
        "ip": None,
        "message": msg,
        "raw": raw,
    }


# ----------------------------
# Main seeding logic
# ----------------------------
def seed(
    base_url: str,
    total: int,
    brute_force: bool,
    brute_ip: str,
    brute_count: int,
    window_seconds: int,
    timeout: int,
    dry_run: bool,
):
    ingest_url = base_url.rstrip("/") + "/api/v1/ingest"

    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=10)  # spread events over last 10 min

    sent = 0
    ok = 0
    failed = 0

    # 1) Optional: generate a brute-force burst within the last window
    if brute_force:
        # ensure these happen very recently
        burst_end = now
        burst_start = now - timedelta(seconds=window_seconds)
        for i in range(brute_count):
            ts = burst_start + (burst_end - burst_start) * (i / max(brute_count - 1, 1))
            ev = make_auth_event(
                ts=ts,
                source="linux",
                ip=brute_ip,
                user=random.choice(USERS),
                host=random.choice(HOSTS),
                success=False,
            )
            if dry_run:
                print(json.dumps(ev, indent=2))
                ok += 1
            else:
                status, body = post_json(ingest_url, ev, timeout=timeout)
                if status == 200:
                    ok += 1
                else:
                    failed += 1
                    print(f"[!] brute event failed: HTTP {status} - {body}")
            sent += 1

    # 2) Generate background events
    sources = ["linux", "windows", "app"]
    event_types = ["authentication", "network", "process"]

    while sent < total:
        ts = start + (now - start) * (random.random())
        source = random.choice(sources)
        et = random.choice(event_types)

        host = random.choice(HOSTS)
        user = random.choice(USERS)
        ip = gen_ip("192.168.1.", random.randint(2, 254))

        if et == "authentication":
            success = random.random() < 0.7  # 70% success
            ev = make_auth_event(ts, source, ip, user, host, success)
        elif et == "network":
            ev = make_network_event(ts, source, ip, host)
        else:
            ev = make_process_event(ts, source, host, user)

        if dry_run:
            print(json.dumps(ev, indent=2))
            ok += 1
        else:
            status, body = post_json(ingest_url, ev, timeout=timeout)
            if status == 200:
                ok += 1
            else:
                failed += 1
                print(f"[!] event failed: HTTP {status} - {body}")

        sent += 1

    print("\n=== Seed summary ===")
    print(f"Target events: {total}")
    print(f"Sent: {sent}")
    print(f"OK: {ok}")
    print(f"Failed: {failed}")
    print(f"Ingest endpoint: {ingest_url}")


def main():
    parser = argparse.ArgumentParser(description="Mini-SIEM seed script via /api/v1/ingest")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="FastAPI base URL")
    parser.add_argument("--total", type=int, default=200, help="Total number of events to send")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout seconds")
    parser.add_argument("--dry-run", action="store_true", help="Print events instead of sending")

    # brute force options
    parser.add_argument("--bruteforce", action="store_true", help="Generate a brute-force burst")
    parser.add_argument("--brute-ip", default="192.168.1.10", help="IP to use for brute force burst")
    parser.add_argument("--brute-count", type=int, default=6, help="How many failed auth events in the burst")
    parser.add_argument("--window-seconds", type=int, default=50, help="Burst time window (seconds)")

    args = parser.parse_args()

    seed(
        base_url=args.base_url,
        total=args.total,
        brute_force=args.bruteforce,
        brute_ip=args.brute_ip,
        brute_count=args.brute_count,
        window_seconds=args.window_seconds,
        timeout=args.timeout,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()