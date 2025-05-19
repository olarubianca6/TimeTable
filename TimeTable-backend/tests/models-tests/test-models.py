import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.extension import db
from app.models import *

TEST_DATABASE_URI = 'sqlite:///:memory:'
engine = create_engine(TEST_DATABASE_URI)
Session = sessionmaker(bind=engine)

db.metadata.create_all(bind=engine)


@pytest.fixture(scope='function')
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def test_invalid_discipline(session):
    with pytest.raises(Exception):
        invalid = Discipline(name=None, year_id=None)
        session.add(invalid)
        session.commit()


def test_invalid_teacher(session):
    with pytest.raises(Exception):
        invalid = Teacher(name=None)
        session.add(invalid)
        session.commit()


def test_invalid_group(session):
    with pytest.raises(Exception):
        invalid = Group(name=None, year_id=None, semian_id=None)
        session.add(invalid)
        session.commit()


def test_invalid_class_session(session):
    with pytest.raises(Exception):
        invalid = ClassSession(
            discipline_id=None,
            teacher_id=None,
            room_id=None,
            time_slot_id=None,
            semian_id=None,
            group_id=None,
            class_type=None
        )
        session.add(invalid)
        session.commit()


def test_invalid_room(session):
    with pytest.raises(Exception):
        invalid = Room(name=None, room_type=None)
        session.add(invalid)
        session.commit()


def test_invalid_student(session):
    with pytest.raises(Exception):
        invalid = Student(name=None)
        session.add(invalid)
        session.commit()


def test_invalid_time_slot(session):
    with pytest.raises(Exception):
        invalid = TimeSlot(day=None, start_time=None, end_time=None)
        session.add(invalid)
        session.commit()


def test_invalid_year(session):
    with pytest.raises(Exception):
        invalid = Year(name=None)
        session.add(invalid)
        session.commit()


def test_invalid_semian(session):
    with pytest.raises(Exception):
        invalid = Semian(name=None, year_id=None)
        session.add(invalid)
        session.commit()


def test_invalid_discipline_teacher(session):
    with pytest.raises(Exception):
        invalid = DisciplineTeacher(teacher_id=None, discipline_id=None)
        session.add(invalid)
        session.commit()
