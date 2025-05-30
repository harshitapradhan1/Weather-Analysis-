import unittest
from utils.helpers import analyze_data

class TestHelpers(unittest.TestCase):
    def test_analyze_data(self):
        sample_data = [
            {"city": "A", "temperature": 10, "humidity": 80, "description": "clear sky", "wind_speed": 2},
            {"city": "B", "temperature": 30, "humidity": 50, "description": "haze", "wind_speed": 3},
            {"city": "C", "temperature": 20, "humidity": 60, "description": "clear sky", "wind_speed": 1}
        ]
        result = analyze_data(sample_data)
        self.assertIn("City with highest temperature: B", result)
        self.assertIn("City with lowest temperature: A", result)
        self.assertIn("Cities with clear sky or similar: 2", result)

if __name__ == '__main__':
    unittest.main()

