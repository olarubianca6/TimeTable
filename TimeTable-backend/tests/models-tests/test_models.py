import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import create_app, db
from app.config import TestingConfig
from app.models import Discipline, Teacher, Group, ClassSession, Room, Student, TimeSlot, Year, Semian, DisciplineTeacher


class TestModelConstraints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_invalid_discipline(self):
        with self.assertRaises(Exception):
            invalid = Discipline(name=None, year_id=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_teacher(self):
        with self.assertRaises(Exception):
            invalid = Teacher(name=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_group(self):
        with self.assertRaises(Exception):
            invalid = Group(name=None, year_id=None, semian_id=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_class_session(self):
        with self.assertRaises(Exception):
            invalid = ClassSession(
                discipline_id=None,
                teacher_id=None,
                room_id=None,
                time_slot_id=None,
                semian_id=None,
                group_id=None,
                class_type=None
            )
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_room(self):
        with self.assertRaises(Exception):
            invalid = Room(name=None, room_type=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_student(self):
        with self.assertRaises(Exception):
            invalid = Student(name=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_time_slot(self):
        with self.assertRaises(Exception):
            invalid = TimeSlot(day=None, start_time=None, end_time=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_year(self):
        with self.assertRaises(Exception):
            invalid = Year(name=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_semian(self):
        with self.assertRaises(Exception):
            invalid = Semian(name=None, year_id=None)
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_discipline_teacher(self):
        with self.assertRaises(Exception):
            invalid = DisciplineTeacher(teacher_id=None, discipline_id=None)
            db.session.add(invalid)
            db.session.commit()

if __name__ == "__main__":
    unittest.main()
