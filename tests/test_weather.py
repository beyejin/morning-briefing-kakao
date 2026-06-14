import unittest

from morning_briefing.weather import build_weather_from_current_and_forecast


class WeatherTests(unittest.TestCase):
    def test_builds_weather_summary_from_free_openweather_endpoints(self):
        current = {
            "weather": [{"description": "흐림"}],
            "main": {"temp": 21.2, "feels_like": 22.4},
            "wind": {"speed": 3.1},
        }
        forecast = {
            "list": [
                {"dt_txt": "2026-06-14 00:00:00", "main": {"temp_min": 19.1, "temp_max": 22.0}, "pop": 0.2},
                {"dt_txt": "2026-06-14 03:00:00", "main": {"temp_min": 20.0, "temp_max": 26.8}, "pop": 0.6},
                {"dt_txt": "2026-06-15 00:00:00", "main": {"temp_min": 18.0, "temp_max": 24.0}, "pop": 0.9},
            ]
        }

        weather = build_weather_from_current_and_forecast(current, forecast, "2026-06-14")

        self.assertEqual(weather.description, "흐림")
        self.assertEqual(weather.current_temp, 21.2)
        self.assertEqual(weather.feels_like, 22.4)
        self.assertEqual(weather.min_temp, 19.1)
        self.assertEqual(weather.max_temp, 26.8)
        self.assertEqual(weather.rain_chance, 0.6)
        self.assertEqual(weather.wind_speed, 3.1)


if __name__ == "__main__":
    unittest.main()
