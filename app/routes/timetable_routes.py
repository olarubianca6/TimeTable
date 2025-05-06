from flask import Blueprint, render_template
from app.models import ClassSession, Teacher, Discipline, Room, TimeSlot

timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/timetable', methods=['GET'])
def timetable():
    class_sessions = ClassSession.query.all()
    timetable_data = []

    for class_session in class_sessions:
        discipline = Discipline.query.get(class_session.discipline_id)
        teacher = Teacher.query.get(class_session.teacher_id)
        room = Room.query.get(class_session.room_id)
        time_slot = TimeSlot.query.get(class_session.time_slot_id)

        timetable_data.append({
            'discipline': discipline.name if discipline else None,
            'teacher': teacher.name if teacher else None,
            'room': room.name if room else None,
            'time_slot': time_slot.slot if time_slot else None,
            'class_type': class_session.class_type
        })

    return render_template('timetable.html', timetable_data=timetable_data)