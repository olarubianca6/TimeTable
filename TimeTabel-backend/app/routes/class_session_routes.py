from flask import request, jsonify, Blueprint
from app.extension import db
from app.models import ClassSession, Teacher, Discipline, Room, TimeSlot
from app.logic.conflict_checker import room_conflict, teacher_conflict, group_conflict
from app.logic.restrictions import valid_class_time, match_room_class_type

class_session_bp = Blueprint('class_session', __name__)

def check_conflicts(existing_class_sessions, class_session):
    if room_conflict(existing_class_sessions, class_session):
        return {'error': 'Room conflict'}, 400

    if teacher_conflict(existing_class_sessions, class_session):
        return {'error': 'Teacher conflict'}, 400

    if group_conflict(existing_class_sessions, class_session):
        return {'error': 'Group conflict'}, 400

    return None, None

@class_session_bp.route('/class_sessions', methods=['GET'])
def get_all_class_sessions():
    year_id = request.args.get('year_id')

    class_sessions_query = ClassSession.query
    if year_id:
        class_sessions_query = class_sessions_query.join(Discipline).filter(Discipline.year_id == year_id)

    class_sessions = class_sessions_query.all()
    print(class_sessions)
    if not class_sessions:
        return jsonify({'message': 'No class sessions found'}), 404

    response = []
    for class_session in class_sessions:
        discipline = Discipline.query.get(class_session.discipline_id)
        teacher = Teacher.query.get(class_session.teacher_id)
        room = Room.query.get(class_session.room_id)
        time_slot = TimeSlot.query.get(class_session.time_slot_id)
        time_slot_str = f"{time_slot.start_time.strftime('%H:%M')} - {time_slot.end_time.strftime('%H:%M')}" if time_slot else None
        response.append({
            'id': class_session.id,
            'discipline': discipline.name if discipline else None,
            'teacher': teacher.name if teacher else None,
            'room': room.name if room else None,
            'day': time_slot.day if time_slot else None,
            'time_slot': time_slot_str,
            'class_type': class_session.class_type
        })
    return jsonify(response), 200

@class_session_bp.route('/class_session/<int:id>', methods=['GET'])
def get_class_session(id):
    class_session = ClassSession.query.get(id)
    if not class_session:
        return jsonify({'error': 'Class session not found'}), 404

    discipline = Discipline.query.get(class_session.discipline_id)
    teacher = Teacher.query.get(class_session.teacher_id)
    room = Room.query.get(class_session.room_id)
    time_slot = TimeSlot.query.get(class_session.time_slot_id)

    response = {
        'id': class_session.id,
        'discipline': discipline.name if discipline else None,
        'teacher': teacher.name if teacher else None,
        'room': room.name if room else None,
        'time_slot': time_slot.slot if time_slot else None,
        'class_type': class_session.class_type
    }

    return jsonify(response), 200

@class_session_bp.route('/add_class_session', methods=['POST'])
def add_class_session():
    data = request.get_json()

    discipline_id = data.get('discipline_id')
    teacher_id = data.get('teacher_id')
    room_id = data.get('room_id')
    time_slot_id = data.get('time_slot_id')
    class_type = data.get('class_type')

    discipline = Discipline.query.get(discipline_id)
    teacher = Teacher.query.get(teacher_id)
    room = Room.query.get(room_id)
    time_slot = TimeSlot.query.get(time_slot_id)

    if not discipline or not teacher or not room or not time_slot:
        return jsonify({'error': 'Invalid data provided'}), 400

    # if not valid_class_time(time_slot.day, time_slot.hour):
    #     return jsonify({'error': 'Invalid class time'}), 400
    if not match_room_class_type(room.room_type, class_type):
        return jsonify({'error': 'Room type does not match class type'}), 400

    existing_class_sessions = ClassSession.query.all()
    new_class_session = ClassSession(
        discipline=discipline,
        teacher_id=teacher_id,
        room_id=room_id,
        time_slot_id=time_slot_id,
        class_type=class_type
    )
    if existing_class_sessions:
        conflict_response, status_code = check_conflicts(existing_class_sessions, new_class_session)
        if conflict_response:
            return jsonify(conflict_response), status_code

    db.session.add(new_class_session)
    db.session.commit()

    return jsonify({'message': 'Class session added successfully'}), 201

@class_session_bp.route('/edit_class_session/<int:id>', methods=['PUT'])
def edit_class_session(id):
    data = request.get_json()

    class_session = ClassSession.query.get(id)
    if not class_session:
        return jsonify({'error': 'Class session not found'}), 404

    class_session.discipline_id = data.get('discipline_id', class_session.discipline_id)
    class_session.teacher_id = data.get('teacher_id', class_session.teacher_id)
    class_session.room_id = data.get('room_id', class_session.room_id)
    class_session.time_slot_id = data.get('time_slot_id', class_session.time_slot_id)
    class_session.class_type = data.get('class_type', class_session.class_type)

    room = Room.query.get(class_session.room_id)
    time_slot = TimeSlot.query.get(class_session.time_slot_id)

    if not valid_class_time(time_slot.day, time_slot.hour):
        return jsonify({'error': 'Invalid class time'}), 400
    if not match_room_class_type(room.room_type, class_session.class_type):
        return jsonify({'error': 'Room type does not match class type'}), 400

    existing_class_sessions = ClassSession.query.all()
    conflict_response, status_code = check_conflicts(existing_class_sessions, class_session)
    if conflict_response:
        return jsonify(conflict_response), status_code

    db.session.commit()

    return jsonify({'message': 'Class session updated successfully'}), 200

@class_session_bp.route('/delete_class_session/<int:id>', methods=['DELETE'])
def delete_class_session(id):
    class_session = ClassSession.query.get(id)
    if not class_session:
        return jsonify({'error': 'Class session not found'}), 404

    db.session.delete(class_session)
    db.session.commit()

    return jsonify({'message': 'Class session deleted successfully'}), 200