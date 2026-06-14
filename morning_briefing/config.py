from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    timezone: str
    latitude: float | None
    longitude: float | None
    openweather_api_key: str | None
    calendar_ics_urls: list[str]
    kakao_access_token: str | None
    rss_feeds: list[str]
    dry_run: bool


def load_settings() -> Settings:
    return Settings(
        timezone=os.getenv("BRIEFING_TIMEZONE", "Asia/Seoul"),
        latitude=_coordinate_env("BRIEFING_LATITUDE", "LATITUDE"),
        longitude=_coordinate_env("BRIEFING_LONGITUDE", "LONGITUDE"),
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY"),
        calendar_ics_urls=_calendar_ics_urls(),
        kakao_access_token=os.getenv("KAKAO_ACCESS_TOKEN"),
        rss_feeds=_rss_feeds(),
        dry_run=os.getenv("DRY_RUN", "").lower() in {"1", "true", "yes"},
    )


def _float_env(name: str) -> float | None:
    value = os.getenv(name)
    if not value:
        return None
    return float(value)


def _coordinate_env(primary_name: str, fallback_name: str) -> float | None:
    return _float_env(primary_name) if os.getenv(primary_name) else _float_env(fallback_name)


def _calendar_ics_urls() -> list[str]:
    raw = (
        os.getenv("ICLOUD_CALENDAR_ICS_URLS")
        or os.getenv("ICLOUD_CALENDAR_ICS_URL")
        or os.getenv("CALENDAR_ICS_URLS")
        or os.getenv("CALENDAR_ICS_URL")
        or os.getenv("GOOGLE_CALENDAR_ICS_URL")
    )
    if not raw:
        return []
    return [_normalize_calendar_url(value.strip()) for value in raw.split(",") if value.strip()]


def _normalize_calendar_url(value: str) -> str:
    if value and value.startswith("webcal://"):
        return "https://" + value.removeprefix("webcal://")
    return value


def _rss_feeds() -> list[str]:
    raw = os.getenv("RSS_FEEDS")
    if raw:
        return [feed.strip() for feed in raw.split(",") if feed.strip()]
    return ["https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"]
