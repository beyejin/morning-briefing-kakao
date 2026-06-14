from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    timezone: str
    latitude: float | None
    longitude: float | None
    openweather_api_key: str | None
    google_calendar_ics_url: str | None
    kakao_access_token: str | None
    rss_feeds: list[str]
    dry_run: bool


def load_settings() -> Settings:
    return Settings(
        timezone=os.getenv("BRIEFING_TIMEZONE", "Asia/Seoul"),
        latitude=_float_env("LATITUDE"),
        longitude=_float_env("LONGITUDE"),
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY"),
        google_calendar_ics_url=os.getenv("GOOGLE_CALENDAR_ICS_URL"),
        kakao_access_token=os.getenv("KAKAO_ACCESS_TOKEN"),
        rss_feeds=_rss_feeds(),
        dry_run=os.getenv("DRY_RUN", "").lower() in {"1", "true", "yes"},
    )


def _float_env(name: str) -> float | None:
    value = os.getenv(name)
    if not value:
        return None
    return float(value)


def _rss_feeds() -> list[str]:
    raw = os.getenv("RSS_FEEDS")
    if raw:
        return [feed.strip() for feed in raw.split(",") if feed.strip()]
    return ["https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"]

