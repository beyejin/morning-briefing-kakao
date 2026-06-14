from __future__ import annotations

from datetime import datetime

from morning_briefing.http import HttpError, get_json
from morning_briefing.models import AirQuality, WeatherSummary


AIR_LABELS = {
    1: "좋음",
    2: "보통",
    3: "약간 나쁨",
    4: "나쁨",
    5: "매우 나쁨",
}


def fetch_weather(lat: float | None, lon: float | None, api_key: str | None) -> WeatherSummary | None:
    if lat is None or lon is None or not api_key:
        return None
    try:
        data = get_json(
            "https://api.openweathermap.org/data/3.0/onecall",
            {
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "units": "metric",
                "lang": "kr",
                "exclude": "minutely,hourly,alerts",
            },
        )
        return build_weather_from_onecall(data)
    except HttpError:
        return fetch_weather_fallback(lat, lon, api_key)


def build_weather_from_onecall(data: dict) -> WeatherSummary:
    current = data.get("current", {})
    daily = (data.get("daily") or [{}])[0]
    temp = daily.get("temp", {})
    weather_items = current.get("weather") or daily.get("weather") or [{}]
    rain_chance = float(daily.get("pop", 0) or 0)

    return WeatherSummary(
        description=str(weather_items[0].get("description", "날씨 정보 없음")),
        current_temp=float(current.get("temp", 0)),
        feels_like=float(current.get("feels_like", current.get("temp", 0))),
        min_temp=float(temp.get("min", current.get("temp", 0))),
        max_temp=float(temp.get("max", current.get("temp", 0))),
        rain_chance=rain_chance,
        wind_speed=float(current.get("wind_speed", 0)),
    )


def fetch_weather_fallback(lat: float, lon: float, api_key: str) -> WeatherSummary | None:
    try:
        current = get_json(
            "https://api.openweathermap.org/data/2.5/weather",
            {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "kr"},
        )
        forecast = get_json(
            "https://api.openweathermap.org/data/2.5/forecast",
            {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "kr"},
        )
    except HttpError:
        return None

    today = _local_weather_date(current, forecast)
    return build_weather_from_current_and_forecast(current, forecast, today)


def build_weather_from_current_and_forecast(current: dict, forecast: dict, today: str) -> WeatherSummary:
    weather_items = current.get("weather") or [{}]
    main = current.get("main", {})
    wind = current.get("wind", {})
    today_items = [
        item for item in forecast.get("list", []) if str(item.get("dt_txt", "")).startswith(today)
    ]

    min_temps = [_float(item.get("main", {}).get("temp_min")) for item in today_items]
    max_temps = [_float(item.get("main", {}).get("temp_max")) for item in today_items]
    rain_chances = [_float(item.get("pop")) for item in today_items]

    current_temp = _float(main.get("temp"))
    return WeatherSummary(
        description=str(weather_items[0].get("description", "날씨 정보 없음")),
        current_temp=current_temp,
        feels_like=_float(main.get("feels_like", current_temp)),
        min_temp=min(min_temps) if min_temps else _float(main.get("temp_min", current_temp)),
        max_temp=max(max_temps) if max_temps else _float(main.get("temp_max", current_temp)),
        rain_chance=max(rain_chances) if rain_chances else 0.0,
        wind_speed=_float(wind.get("speed")),
    )


def fetch_air_quality(lat: float | None, lon: float | None, api_key: str | None) -> AirQuality | None:
    if lat is None or lon is None or not api_key:
        return None
    try:
        data = get_json(
            "https://api.openweathermap.org/data/2.5/air_pollution",
            {"lat": lat, "lon": lon, "appid": api_key},
        )
    except HttpError:
        return None

    item = (data.get("list") or [{}])[0]
    index = int(item.get("main", {}).get("aqi", 0) or 0)
    components = item.get("components", {})
    return AirQuality(
        index=index,
        label=AIR_LABELS.get(index, "알 수 없음"),
        pm10=_optional_float(components.get("pm10")),
        pm25=_optional_float(components.get("pm2_5")),
    )


def _optional_float(value: object) -> float | None:
    if value is None:
        return None
    return float(value)


def _float(value: object) -> float:
    if value is None:
        return 0.0
    return float(value)


def _local_weather_date(current: dict, forecast: dict) -> str:
    timestamp = int(current.get("dt", 0) or 0)
    offset_seconds = int(forecast.get("city", {}).get("timezone", 0) or 0)
    if timestamp:
        return datetime.utcfromtimestamp(timestamp + offset_seconds).strftime("%Y-%m-%d")

    first_forecast = (forecast.get("list") or [{}])[0]
    return str(first_forecast.get("dt_txt", "")).split(" ", maxsplit=1)[0]
