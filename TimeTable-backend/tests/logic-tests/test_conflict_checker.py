import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import create_app, db
from app.config import TestingConfig
from app.models import Discipline, ClassSession, DisciplineTeacher, Group, Semian, Year
from app.logic.conflict_checker import room_conflict, teacher_conflict, group_conflict, semian_conflict

class TestConflictChecker(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.year1 = Year(id=1, name="Year 1")
        db.session.add(self.year1)
        db.session.commit()

        self.semian1 = Semian(id=1, name="S1", year_id=self.year1.id)
        self.semian2 = Semian(id=2, name="S2", year_id=self.year1.id)
        db.session.add_all([self.semian1, self.semian2])
        db.session.commit()

        self.group1 = Group(id=1, name="G1", year_id=self.year1.id, semian_id=self.semian1.id)
        self.group2 = Group(id=2, name="G2", year_id=self.year1.id, semian_id=self.semian2.id)
        db.session.add_all([self.group1, self.group2])
        db.session.commit()

        self.discipline1 = Discipline(id=1, name="Math", year_id=self.year1.id)
        self.discipline2 = Discipline(id=2, name="Physics", year_id=self.year1.id)
        db.session.add_all([self.discipline1, self.discipline2])
        db.session.commit()

        db.session.add_all([
            DisciplineTeacher(discipline_id=1, teacher_id=1),
            DisciplineTeacher(discipline_id=2, teacher_id=2)
        ])
        db.session.commit()

        self.discipline1.groups = [self.group1]

        self.existing_entries = [
            ClassSession(
                room_id=101,
                time_slot_id=1,
                discipline_id=1,
                teacher_id=1,
                group_id=1,
                semian_id=1,
                class_type="course"
            ),
            ClassSession(
                room_id=202,
                time_slot_id=2,
                discipline_id=2,
                teacher_id=2,
                group_id=2,
                semian_id=2,
                class_type="seminar"
            )
        ]
        db.session.add_all(self.existing_entries)
        db.session.commit()

        self.new_entry = ClassSession(
            room_id=101,
            time_slot_id=1,
            discipline_id=1,
            teacher_id=1,
            group_id=1,
            semian_id=1,
            class_type="course"
        )
        self.new_entry.discipline = self.discipline1

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_room_conflict(self):
        self.assertTrue(room_conflict(self.existing_entries, self.new_entry))

    def test_teacher_conflict(self):
        self.assertTrue(teacher_conflict(self.existing_entries, self.new_entry))

    def test_group_conflict(self):
        self.assertTrue(group_conflict(self.existing_entries, self.new_entry))

    def test_semian_conflict(self):
        self.assertTrue(semian_conflict(self.existing_entries, self.new_entry))

if __name__ == "__main__":
    unittest.main()
