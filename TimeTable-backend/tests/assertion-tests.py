from datetime import time

import pytest
from app.models import Room, Teacher
from app.logic.restrictions import match_room_class_type, valid_class_time


def test_valid_room():
    room = Room(name="212", room_type="course")
    assert room.name == "212"

def test_invalid_room():
    with pytest.raises(AssertionError):
        Room(name="200", room_type="gym")

def test_valid_teacher():
    teacher = Teacher(name="Olaru")
    assert teacher.name == "Olaru"

def test_invalid_teacher():
    with pytest.raises(AssertionError):
        Teacher(name="")

def test_match_course_room():
    assert match_room_class_type("course", "course") is True

def test_match_invalid_room():
    assert match_room_class_type("seminar", "laboratory") is False

def test_invalid_class_time():
    with pytest.raises(AssertionError):
        valid_class_time(None, time(10, 0))

    with pytest.raises(AssertionError):
        valid_class_time("Monday", None)

    with pytest.raises(AssertionError):
        valid_class_time(123, time(10, 0))