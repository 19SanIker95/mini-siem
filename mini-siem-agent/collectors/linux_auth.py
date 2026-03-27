import os
import re
import time
import subprocess
from datetime import datetime, timezone

FAILED_PATTERNS = [
    re.compile(r"Failed password for (invalid user )?(?P<user>[\w\-\.\@]+) from (?P<ip>\d+\.\d+\.\d+\.\d+)"),
    re.compile(r"authentication failure.*rhost=(?P<ip>\d+\.\d+\.\d+\.\d+).*user=(?P<user>[\w\-\.\@]+)"),
    re.compile(r"invalid user (?P<user>[\w\-\.\@]+) from (?P<ip>\d+\.\d+\.\d+\.\d+)", re.IGNORECASE),
]


def build_event(user, ip, raw_line, source, host):
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "event_type": "authentication",
        "severity": 3,
        "host": host,
        "user": user,
        "ip": ip,
        "message": "Failed SSH login attempt",
        "raw": {
            "log": raw_line,
            "service": "sshd"
        }
    }


# -------- MODE 1: auth.log --------
def authlog_collector(send_event, host, source, log_path):
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            for pattern in FAILED_PATTERNS:
                m = pattern.search(line)
                if m:
                    send_event(
                        build_event(
                            m.group("user"),
                            m.group("ip"),
                            line.strip(),
                            source,
                            host
                        )
                    )


# -------- MODE 2: journald --------
def journald_collector(send_event, host, source):
    cmd = [
        "journalctl",
        "-u", "ssh.service",
        "-f",
        "-o", "cat"
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in proc.stdout:
        for pattern in FAILED_PATTERNS:
            m = pattern.search(line)
            if m:
                send_event(
                    build_event(
                        m.group("user"),
                        m.group("ip"),
                        line.strip(),
                        source,
                        host
                    )
                )


def start_linux_auth(send_event, config, host):
    source = config.get("source", "linux")
    mode = config.get("mode", "authlog")

    if mode == "journald":
        journald_collector(send_event, host, source)
    else:
        log_path = config.get("auth_log_path", "/var/log/auth.log")
        authlog_collector(send_event, host, source, log_path)