from __future__ import annotations

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
    except HttpError:
        return None

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

