from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from morning_briefing.models import CalendarEvent


def parse_ics_events(ics_text: str, target_date: date, timezone_name: str) -> list[CalendarEvent]:
    zone = ZoneInfo(timezone_name)
    events: list[CalendarEvent] = []

    for block in _event_blocks(ics_text):
        summary = _field(block, "SUMMARY") or "제목 없는 일정"
        start_value = _field(block, "DTSTART")
        if not start_value:
            continue

        start = _parse_ics_datetime(start_value, zone)
        if start.date() != target_date:
            continue

        events.append(CalendarEvent(summary=_unescape(summary), time_text=start.strftime("%H:%M")))

    return sorted(events, key=lambda event: event.time_text)


def _event_blocks(ics_text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for raw_line in _unfold_lines(ics_text):
        line = raw_line.strip()
        if line == "BEGIN:VEVENT":
            current = []
        elif line == "END:VEVENT":
            if current is not None:
                blocks.append(current)
            current = None
        elif current is not None:
            current.append(line)
    return blocks


def _unfold_lines(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        if line.startswith((" ", "\t")) and lines:
            lines[-1] += line[1:]
        else:
            lines.append(line)
    return lines


def _field(block: list[str], name: str) -> str | None:
    prefix = f"{name}"
    for line in block:
        if line.startswith(prefix):
            _, value = line.split(":", 1)
            return value
    return None


def _parse_ics_datetime(value: str, zone: ZoneInfo) -> datetime:
    if len(value) == 8:
        return datetime.strptime(value, "%Y%m%d").replace(tzinfo=zone)
    if value.endswith("Z"):
        parsed = datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        return parsed.astimezone(zone)
    return datetime.strptime(value, "%Y%m%dT%H%M%S").replace(tzinfo=zone)


def _unescape(value: str) -> str:
    return value.replace("\\,", ",").replace("\\n", " ").replace("\\;", ";")

