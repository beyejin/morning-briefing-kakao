from __future__ import annotations

import random
from datetime import datetime
from zoneinfo import ZoneInfo

from morning_briefing.calendar import parse_ics_events
from morning_briefing.config import load_settings
from morning_briefing.formatter import format_briefing
from morning_briefing.http import HttpError, get_text
from morning_briefing.kakao import send_to_me
from morning_briefing.news import fetch_news
from morning_briefing.outfit import recommend_outfit
from morning_briefing.weather import fetch_air_quality, fetch_weather

AFFIRMATIONS = [
    "나는 오늘 필요한 만큼 차분하고 단단하다.",
    "나는 작은 일부터 하나씩 해낼 수 있다.",
    "오늘의 나는 어제보다 조금 더 나를 믿는다.",
    "나는 급하지 않아도 충분히 앞으로 가고 있다.",
    "내 속도는 나에게 맞고, 그걸로 충분하다.",
]


def build_briefing() -> str:
    settings = load_settings()
    today = datetime.now(ZoneInfo(settings.timezone)).date()

    weather = fetch_weather(settings.latitude, settings.longitude, settings.openweather_api_key)
    air = fetch_air_quality(settings.latitude, settings.longitude, settings.openweather_api_key)
    events = _fetch_events(settings.google_calendar_ics_url, today, settings.timezone)
    news = fetch_news(settings.rss_feeds)
    affirmation = random.choice(AFFIRMATIONS)
    outfit = recommend_outfit(weather, air)

    return format_briefing(today, weather, air, events, news, affirmation, outfit)


def main() -> int:
    settings = load_settings()
    message = build_briefing()
    print(message)

    if settings.dry_run:
        return 0
    if not settings.kakao_access_token:
        raise RuntimeError("KAKAO_ACCESS_TOKEN is required unless DRY_RUN=true.")
    send_to_me(settings.kakao_access_token, message)
    return 0


def _fetch_events(calendar_url: str | None, today, timezone_name: str):
    if not calendar_url:
        return []
    try:
        return parse_ics_events(get_text(calendar_url), today, timezone_name)
    except HttpError:
        return []


if __name__ == "__main__":
    raise SystemExit(main())
