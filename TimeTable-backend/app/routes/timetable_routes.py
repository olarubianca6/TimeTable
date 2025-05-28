from flask import Blueprint, render_template
from app.models import ClassSession, Teacher, Discipline, Room, TimeSlot

timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/timetable', methods=['GET'])
def timetable():
    class_sessions = ClassSession.query.all()

    assert isinstance(class_sessions, list), "Expected list of class sessions"

    timetable_data = []
    n = len(class_sessions)

    for i, class_session in enumerate(class_sessions):
      
        assert (n - i) > 0, "Loop variant condition failed"

        discipline = Discipline.query.get(class_session.discipline_id)
        teacher = Teacher.query.get(class_session.teacher_id)
        room = Room.query.get(class_session.room_id)
        time_slot = TimeSlot.query.get(class_session.time_slot_id)

        
        if discipline:
            assert hasattr(discipline, 'name'), "Discipline missing 'name'"
        if teacher:
            assert hasattr(teacher, 'name'), "Teacher missing 'name'"
        if room:
            assert hasattr(room, 'name'), "Room missing 'name'"
        if time_slot:
            assert hasattr(time_slot, 'day') and hasattr(time_slot, 'start_time') and hasattr(time_slot, 'end_time'), "TimeSlot missing attributes"

        timetable_data.append({
            'discipline': discipline.name if discipline else None,
            'teacher': teacher.name if teacher else None,
            'room': room.name if room else None,
            'time_slot': f"{time_slot.day}: {time_slot.start_time} - {time_slot.end_time}" if time_slot else None,
            'class_type': class_session.class_type
        })


    assert all('discipline' in entry and 'time_slot' in entry for entry in timetable_data), "Malformed timetable entry"

    return render_template('timetable.html', timetable_data=timetable_data)
