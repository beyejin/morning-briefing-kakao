from __future__ import annotations

from morning_briefing.models import AirQuality, WeatherSummary


def recommend_outfit(weather: WeatherSummary | None, air: AirQuality | None) -> str:
    if weather is None:
        return "날씨 정보를 못 가져왔어. 얇게 겹쳐 입고, 밖에 나가기 전에 하늘만 한 번 확인하자."

    base_temp = min(weather.feels_like, weather.min_temp)
    pieces: list[str] = []

    if base_temp <= 4:
        pieces.append("패딩이나 두꺼운 코트")
        pieces.append("니트/기모 이너")
    elif base_temp <= 9:
        pieces.append("코트나 두꺼운 자켓")
        pieces.append("긴팔 이너")
    elif base_temp <= 16:
        pieces.append("가디건이나 얇은 자켓")
        pieces.append("긴팔")
    elif base_temp <= 22:
        pieces.append("가벼운 셔츠")
        pieces.append("얇은 겉옷")
    elif base_temp <= 27:
        pieces.append("반팔이나 얇은 셔츠")
    else:
        pieces.append("통풍 잘 되는 반팔")
        pieces.append("얇은 하의")

    notes: list[str] = []
    if weather.rain_chance >= 0.4:
        notes.append("비 가능성이 있으니 작은 우산도 챙겨")
    if weather.wind_speed >= 5:
        notes.append("바람이 있어서 목을 덮는 아이템이 좋아")
    if air and air.index >= 4:
        notes.append("대기질이 나빠서 마스크를 챙기는 게 좋아")

    outfit = ", ".join(pieces)
    if notes:
        return f"{outfit} 추천. " + " ".join(notes) + "."
    return f"{outfit} 추천."
