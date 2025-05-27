import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import create_app, db
from app.config import TestingConfig  

class TestTeacherEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)  
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_teachers(self):
        with self.app.app_context():
            with patch("app.routes.teacher_routes.Teacher.query") as mock_query:
                mock_query.all.return_value = []
                response = self.client.get("/teachers")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), [])

    def test_get_teacher_by_id_found(self):
        with self.app.app_context():
            with patch("app.routes.teacher_routes.Teacher.query") as mock_query:
                mock_teacher = MagicMock()
                mock_teacher.id = 1
                mock_teacher.name = "Test Teacher"
                mock_query.get.return_value = mock_teacher

                response = self.client.get("/teacher/1")
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertIsInstance(data, dict)
                self.assertEqual(data["id"], 1)
                self.assertEqual(data["name"], "Test Teacher")

    def test_get_teacher_by_id_not_found(self):
        with self.app.app_context():
            with patch("app.routes.teacher_routes.Teacher.query") as mock_query:
                mock_query.get.return_value = None
                response = self.client.get("/teacher/999")
                self.assertEqual(response.status_code, 404)
                data = response.get_json()
                self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
