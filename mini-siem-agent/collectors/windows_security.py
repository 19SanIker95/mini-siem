from datetime import datetime, timezone
import win32evtlog
import winerror

FAIL_ID = 4625

def windows_failed_logon_collector(send_event, source="windows", host=None, poll_seconds=2):
    server = None
    logtype = "Security"
    hand = win32evtlog.OpenEventLog(server, logtype)  # pywin32 docs [10](https://brian3johnson.github.io/pywin32/win32/event.html)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    last_record = None

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            continue

        # O primeiro na leitura backwards é o mais recente
        newest = events[0].RecordNumber
        if last_record is None:
            last_record = newest

        # Processa apenas eventos mais novos do que o último record visto
        for ev in events:
            if ev.RecordNumber <= last_record:
                break

            event_id = winerror.HRESULT_CODE(ev.EventID)
            if event_id != FAIL_ID:
                continue

            # StringInserts varia conforme provider, mas 4625 tem detalhes em XML/fields (ver Microsoft Learn) [4](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625)
            raw = {
                "record": ev.RecordNumber,
                "source": ev.SourceName,
                "strings": ev.StringInserts,
            }

            payload = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "source": source,
                "event_type": "authentication",
                "severity": 3,
                "host": host,
                "user": None,
                "ip": None,
                "message": "Windows failed logon (Event ID 4625)",
                "raw": raw,
            }
            send_event(payload)

        last_record = newest