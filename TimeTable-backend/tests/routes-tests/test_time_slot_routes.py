import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import create_app, db
from app.config import TestingConfig  

class TestTimeSlotsEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)  
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_time_slots(self):
        with self.app.app_context():
            with patch("app.routes.time_slot_routes.TimeSlot.query") as mock_query:
                mock_query.all.return_value = []
                response = self.client.get("/time_slots")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), [])
                
if __name__ == "__main__":
    unittest.main() 