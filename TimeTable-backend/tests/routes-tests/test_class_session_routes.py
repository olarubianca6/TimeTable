import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import create_app, db
from app.config import TestingConfig
from app.models import ClassSession, Discipline, Teacher, Room, TimeSlot

class TestClassSessionRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all_class_sessions_empty(self):
        with patch("app.routes.class_session_routes.ClassSession.query.all", return_value=[]):
            response = self.client.get("/class_sessions")
            self.assertEqual(response.status_code, 404)

    def test_get_class_session_not_found(self):
        with patch("app.routes.class_session_routes.db.session.get", return_value=None):
            response = self.client.get("/class_session/999")
            self.assertEqual(response.status_code, 404)

    def test_get_class_session_found(self):
        cs = MagicMock()
        cs.id = 1
        cs.discipline_id = 1
        cs.teacher_id = 1
        cs.room_id = 1
        cs.time_slot_id = 1
        cs.class_type = "course"
        
        discipline = MagicMock()
        discipline.name = "Math"
        
        teacher = MagicMock()
        teacher.name = "Prof Smith"
        
        room = MagicMock()
        room.name = "Room 101"
        
        time_slot = MagicMock()
        time_slot.slot = "08:00-10:00"
        
        def mock_session_get(model, id):
            if model == ClassSession and id == 1:
                return cs
            elif model == Discipline and id == 1:
                return discipline
            elif model == Teacher and id == 1:
                return teacher
            elif model == Room and id == 1:
                return room
            elif model == TimeSlot and id == 1:
                return time_slot
            return None

        with patch("app.routes.class_session_routes.db.session.get", side_effect=mock_session_get):
            response = self.client.get("/class_session/1")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['discipline'], "Math")
            self.assertEqual(data['teacher'], "Prof Smith")

    def test_add_class_session_invalid_data(self):
        with patch("app.routes.class_session_routes.db.session.get", return_value=None):
            response = self.client.post("/add_class_session", json={
                'discipline_id': 1,
                'teacher_id': 1,
                'room_id': 1,
                'time_slot_id': 1,
                'class_type': 'course'
            })
            self.assertEqual(response.status_code, 400)

    def test_add_class_session_valid(self):
    
        discipline = MagicMock()
        discipline.name = "Math"
        
        teacher = MagicMock()
        teacher.name = "Prof Smith"
        
        room = MagicMock()
        room.name = "Room 101"
        room.room_type = "lab"
        
        time_slot = MagicMock()
        time_slot.day = "Monday"
        time_slot.hour = "08:00"
        
        new_class_session = MagicMock()

        def mock_session_get(model, id):
            if model == Discipline and id == 1:
                return discipline
            elif model == Teacher and id == 1:
                return teacher
            elif model == Room and id == 1:
                return room
            elif model == TimeSlot and id == 1:
                return time_slot
            return None

        with patch("app.routes.class_session_routes.db.session.get", side_effect=mock_session_get), \
             patch("app.routes.class_session_routes.ClassSession", return_value=new_class_session), \
             patch("app.routes.class_session_routes.ClassSession.query.all", return_value=[]), \
             patch("app.routes.class_session_routes.match_room_class_type", return_value=True), \
             patch("app.routes.class_session_routes.db.session.add"), \
             patch("app.routes.class_session_routes.db.session.commit"):
            
            response = self.client.post("/add_class_session", json={
                'discipline_id': 1,
                'teacher_id': 1,
                'room_id': 1,
                'time_slot_id': 1,
                'class_type': 'lab'
            })
            self.assertEqual(response.status_code, 201)

    def test_edit_class_session_not_found(self):
        with patch("app.routes.class_session_routes.db.session.get", return_value=None):
            response = self.client.put("/edit_class_session/999", json={})
            self.assertEqual(response.status_code, 404)

    def test_edit_class_session_conflict(self):

        cs = MagicMock()
        cs.id = 1
        cs.discipline_id = 1
        cs.teacher_id = 1
        cs.room_id = 1
        cs.time_slot_id = 1
        cs.class_type = "lab"
        
        room = MagicMock()
        room.name = "Room 101"
        room.room_type = "lab"
        
        time_slot = MagicMock()
        time_slot.day = "Monday"
        time_slot.hour = "08:00"

  
        def mock_session_get(model, id):
            if model == ClassSession and id == 1:
                return cs
            elif model == Room and id == 1:
                return room
            elif model == TimeSlot and id == 1:
                return time_slot
            return None


        with patch("app.routes.class_session_routes.db.session.get", side_effect=mock_session_get), \
             patch("app.routes.class_session_routes.ClassSession.query.all", return_value=[]), \
             patch("app.routes.class_session_routes.valid_class_time", return_value=True), \
             patch("app.routes.class_session_routes.match_room_class_type", return_value=True), \
             patch("app.routes.class_session_routes.check_conflicts", return_value=({'error': 'Room conflict'}, 400)):
            
            response = self.client.put("/edit_class_session/1", json={
                'discipline_id': 1,
                'teacher_id': 1,
                'room_id': 1,
                'time_slot_id': 1,
                'class_type': 'lab'
            })
            self.assertEqual(response.status_code, 400)

    def test_edit_class_session_success(self):

        cs = MagicMock()
        cs.id = 1
        cs.discipline_id = 1
        cs.teacher_id = 1
        cs.room_id = 1
        cs.time_slot_id = 1
        cs.class_type = "course"
        
        room = MagicMock()
        room.name = "Room 101"
        room.room_type = "lab"
        
        time_slot = MagicMock()
        time_slot.day = "Monday"
        time_slot.hour = "08:00"

        def mock_session_get(model, id):
            if model == ClassSession and id == 1:
                return cs
            elif model == Room and id == 1:
                return room
            elif model == TimeSlot and id == 1:
                return time_slot
            return None

        with patch("app.routes.class_session_routes.db.session.get", side_effect=mock_session_get), \
             patch("app.routes.class_session_routes.ClassSession.query.all", return_value=[]), \
             patch("app.routes.class_session_routes.valid_class_time", return_value=True), \
             patch("app.routes.class_session_routes.match_room_class_type", return_value=True), \
             patch("app.routes.class_session_routes.check_conflicts", return_value=(None, None)), \
             patch("app.routes.class_session_routes.db.session.commit"):
            
            response = self.client.put("/edit_class_session/1", json={
                'discipline_id': 1,
                'teacher_id': 1,
                'room_id': 1,
                'time_slot_id': 1,
                'class_type': 'lab'
            })
            self.assertEqual(response.status_code, 200)

    def test_delete_class_session_not_found(self):
        with patch("app.routes.class_session_routes.db.session.get", return_value=None):
            response = self.client.delete("/delete_class_session/999")
            self.assertEqual(response.status_code, 404)

    def test_delete_class_session_success(self):
        cs = MagicMock()
        cs.id = 1

        with patch("app.routes.class_session_routes.db.session.get", return_value=cs), \
             patch("app.routes.class_session_routes.db.session.delete"), \
             patch("app.routes.class_session_routes.db.session.commit"):
            
            response = self.client.delete("/delete_class_session/1")
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()