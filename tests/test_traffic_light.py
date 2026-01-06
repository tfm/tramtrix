import unittest
from datetime import datetime, timedelta, timezone
from tramtrix.traffic_light import calculate_traffic_light_colour, to_hex_color
from tramtrix import config

class TestTrafficLight(unittest.TestCase):
    def setUp(self):
        # Ensure config defaults are consistent for tests
        # or mock them if we want to test configuration changes.
        # For now, we assume the defaults or env vars set (Time Green Max=6, Amber Max=3, Amber min=2)
        # We can temporarily override them for robustness if needed, 
        # but let's test against the "standard" logic first.
        self.now = datetime.now(timezone.utc)

    def test_to_hex_color(self):
        self.assertEqual(to_hex_color('RED'), 'a83632')
        self.assertEqual(to_hex_color('GREEN'), '03fc14')
        self.assertEqual(to_hex_color('AMBER'), 'fcca03')
        self.assertEqual(to_hex_color('UNKNOWN'), 'ffffff')

    def test_calculate_traffic_light_colour_green(self):
        # 5 minutes from now (should be Green if Max=6, AmberMax=3)
        future_time = self.now + timedelta(minutes=5)
        self.assertEqual(calculate_traffic_light_colour({future_time}), 'GREEN')

    def test_calculate_traffic_light_colour_amber(self):
        # 2.5 minutes from now (should be Amber if AmberMax=3, AmberMin=2)
        future_time = self.now + timedelta(minutes=2.5)
        self.assertEqual(calculate_traffic_light_colour({future_time}), 'AMBER')

    def test_calculate_traffic_light_colour_red_too_close(self):
        # 1 minute from now (should be Red if AmberMin=2)
        future_time = self.now + timedelta(minutes=1)
        self.assertEqual(calculate_traffic_light_colour({future_time}), 'RED')

    def test_calculate_traffic_light_colour_red_too_far(self):
        # 10 minutes from now (should be Red if GreenMax=6)
        future_time = self.now + timedelta(minutes=10)
        self.assertEqual(calculate_traffic_light_colour({future_time}), 'RED')

    def test_calculate_traffic_light_colour_multiple(self):
        # One Red (too far), One Green
        t1 = self.now + timedelta(minutes=10)
        t2 = self.now + timedelta(minutes=4)
        self.assertEqual(calculate_traffic_light_colour({t1, t2}), 'GREEN')

        # One Red (too close), One Amber
        t3 = self.now + timedelta(minutes=1)
        t4 = self.now + timedelta(minutes=2.5)
        self.assertEqual(calculate_traffic_light_colour({t3, t4}), 'AMBER')

if __name__ == '__main__':
    unittest.main()
