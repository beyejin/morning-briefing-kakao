import os
import unittest
from unittest.mock import patch

from morning_briefing.config import load_settings


class ConfigTests(unittest.TestCase):
    def test_briefing_coordinates_override_default_coordinates(self):
        env = {
            "LATITUDE": "37.5665",
            "LONGITUDE": "126.9780",
            "BRIEFING_LATITUDE": "37.2000",
            "BRIEFING_LONGITUDE": "127.0727",
        }

        with patch.dict(os.environ, env, clear=True):
            settings = load_settings()

        self.assertEqual(settings.latitude, 37.2000)
        self.assertEqual(settings.longitude, 127.0727)


if __name__ == "__main__":
    unittest.main()
