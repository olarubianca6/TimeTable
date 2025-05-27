import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import create_app, db
from app.config import TestingConfig  

class TestYearEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)  
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_years(self):
        with self.app.app_context():
            with patch("app.routes.year_routes.Year.query") as mock_query:
                mock_query.all.return_value = []
                response = self.client.get("/years")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), [])
    
    def test_get_year_by_id_found(self):
        with self.app.app_context():
            with patch("app.routes.year_routes.Year.query") as mock_query:
                mock_year = MagicMock()
                mock_year.id = 1
                mock_year.name = "Test Year"
                mock_query.get.return_value = mock_year

                response = self.client.get("/year/1")
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIsInstance(data, dict)
                self.assertEqual(data["id"], 1)
                self.assertEqual(data["name"], "Test Year")
    
    def test_get_year_by_id_not_found(self):
        with self.app.app_context():
            with patch("app.routes.year_routes.Year.query") as mock_query:
                mock_query.get.return_value = None
                response = self.client.get("/year/999")
                self.assertEqual(response.status_code, 404)
                data = response.get_json()
                self.assertIn("error", data)
                
if __name__ == "__main__":
    unittest.main()