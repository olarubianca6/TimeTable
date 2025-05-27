import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import create_app, db
from app.config import TestingConfig

class TestTimetable(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_timetable_returns_html(self):
        with self.app.app_context():
            with patch("app.routes.timetable_routes.ClassSession.query.all", return_value=[]):
                response = self.client.get("/timetable")
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"<html", response.data.lower())

if __name__ == "__main__":
    unittest.main()
