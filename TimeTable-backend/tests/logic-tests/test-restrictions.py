import unittest
from datetime import time
from app.logic.restrictions import valid_class_time, match_room_class_type


class TestRestrictions(unittest.TestCase):

    def test_valid_class_time(self):
        self.assertFalse(valid_class_time("Saturday", time(10, 0)))
        self.assertFalse(valid_class_time("Monday", time(7, 59)))
        self.assertFalse(valid_class_time("Monday", time(20, 1)))
        self.assertFalse(valid_class_time("Monday", "10:00 AM"))

    def test_match_room_class_type(self):
        self.assertFalse(match_room_class_type("course", "laboratory"))
        self.assertFalse(match_room_class_type("seminar", "course"))
        self.assertFalse(match_room_class_type("unknown", "seminar"))
        self.assertFalse(match_room_class_type("seminar", "other"))


if __name__ == '__main__':
    unittest.main()