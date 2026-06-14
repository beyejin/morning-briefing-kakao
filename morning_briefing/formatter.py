from __future__ import annotations

from datetime import date

from morning_briefing.models import AirQuality, CalendarEvent, NewsItem, WeatherSummary


def format_briefing(
    today: date,
    weather: WeatherSummary | None,
    air: AirQuality | None,
    events: list[CalendarEvent],
    news: list[NewsItem],
    affirmation: str,
    outfit: str,
) -> str:
    lines = [f"{today.month}/{today.day} 아침 브리핑", ""]

    lines.append("날씨")
    if weather:
        lines.append(
            f"- {weather.description}, 현재 {weather.current_temp:.0f}도"
            f" / 체감 {weather.feels_like:.0f}도"
            f" / 최저 {weather.min_temp:.0f}도"
            f" / 최고 {weather.max_temp:.0f}도"
        )
    else:
        lines.append("- 날씨 정보를 가져오지 못했어.")

    if air:
        particle_text = []
        if air.pm10 is not None:
            particle_text.append(f"PM10 {air.pm10:.0f}")
        if air.pm25 is not None:
            particle_text.append(f"PM2.5 {air.pm25:.0f}")
        suffix = f" ({', '.join(particle_text)})" if particle_text else ""
        lines.append(f"- 대기질 {air.label}{suffix}")
    else:
        lines.append("- 대기질 정보를 가져오지 못했어.")

    lines.extend(["", "일정"])
    if events:
        lines.extend(f"- {event.time_text} {event.summary}" for event in events)
    else:
        lines.append("- 오늘 등록된 일정이 없어.")

    lines.extend(["", "옷 추천", f"- {outfit}", "", "아침 확언", f"- {affirmation}", "", "오늘의 뉴스"])
    if news:
        lines.extend(f"- {item.title}" for item in news[:5])
    else:
        lines.append("- 뉴스를 가져오지 못했어.")

    return "\n".join(lines)
