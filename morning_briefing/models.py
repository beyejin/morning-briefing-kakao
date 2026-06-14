from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherSummary:
    description: str
    current_temp: float
    feels_like: float
    min_temp: float
    max_temp: float
    rain_chance: float
    wind_speed: float


@dataclass(frozen=True)
class AirQuality:
    index: int
    label: str
    pm10: float | None = None
    pm25: float | None = None


@dataclass(frozen=True)
class CalendarEvent:
    summary: str
    time_text: str


@dataclass(frozen=True)
class NewsItem:
    title: str
    link: str
