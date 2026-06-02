import win32evtlog
import win32con
def read_event_log(log_type="System", max_events=10):
    event_types = [win32con.EVENTLOG_ERROR_TYPE, win32con.EVENTLOG_WARNING_TYPE]
    hand = win32evtlog.OpenEventLog(“localhost”, log_type)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    count = 0
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    while events and count < max_events:
        for event in events:
        if event.EventType in event_types:
        print(f”[{event.TimeGenerated.Format()}] Source: {event.SourceName} | ID: {event.EventID & 0xFFFF}”)
    if event.StringInserts:
    print(f”  Detail: {’ ’.join(event.StringInserts)}”)
    print(”-” * 55)
    count += 1
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    win32evtlog.CloseEventLog(hand)
read_event_log()