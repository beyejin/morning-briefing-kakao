import unittest
from datetime import date

from morning_briefing.calendar import parse_ics_events
from morning_briefing.formatter import format_briefing
from morning_briefing.models import AirQuality, CalendarEvent, NewsItem, WeatherSummary
from morning_briefing.outfit import recommend_outfit


class BriefingCoreTests(unittest.TestCase):
    def test_recommends_layered_outfit_for_cold_bad_air_day(self):
        weather = WeatherSummary(
            description="흐림",
            current_temp=3.0,
            feels_like=0.0,
            min_temp=-2.0,
            max_temp=7.0,
            rain_chance=0.2,
            wind_speed=5.5,
        )
        air = AirQuality(index=4, label="나쁨", pm10=81.0, pm25=36.0)

        result = recommend_outfit(weather, air)

        self.assertIn("패딩", result)
        self.assertIn("마스크", result)
        self.assertIn("바람", result)

    def test_parse_ics_events_returns_events_for_target_day(self):
        ics = """BEGIN:VCALENDAR
BEGIN:VEVENT
SUMMARY:팀 미팅
DTSTART:20260614T010000Z
DTEND:20260614T020000Z
END:VEVENT
BEGIN:VEVENT
SUMMARY:내일 일정
DTSTART:20260615T010000Z
DTEND:20260615T020000Z
END:VEVENT
END:VCALENDAR
"""

        events = parse_ics_events(ics, date(2026, 6, 14), "Asia/Seoul")

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].summary, "팀 미팅")
        self.assertEqual(events[0].time_text, "10:00")

    def test_format_briefing_includes_main_sections(self):
        message = format_briefing(
            today=date(2026, 6, 14),
            weather=WeatherSummary("맑음", 22.4, 22.0, 18.0, 27.0, 0.1, 2.0),
            air=AirQuality(2, "보통", 30.0, 14.0),
            events=[CalendarEvent("점심 약속", "12:30")],
            news=[NewsItem("오늘의 주요 뉴스", "https://example.com")],
            affirmation="나는 차분하게 해낼 수 있다.",
            outfit="가벼운 셔츠와 얇은 겉옷을 추천해.",
        )

        self.assertIn("아침 브리핑", message)
        self.assertIn("체감 22", message)
        self.assertIn("점심 약속", message)
        self.assertIn("오늘의 주요 뉴스", message)
        self.assertIn("나는 차분하게 해낼 수 있다.", message)
        self.assertIn("가벼운 셔츠", message)


if __name__ == "__main__":
    unittest.main()
