from flask import request, jsonify, Blueprint
from app.extension import db
from app.models import ClassSession, Teacher, Discipline, Room, TimeSlot, Semian, Group
from app.logic.conflict_checker import room_conflict, teacher_conflict, group_conflict, semian_conflict
from app.logic.restrictions import valid_class_time, match_room_class_type

class_session_bp = Blueprint('class_session', __name__)


def check_conflicts(existing_class_sessions, class_session):
    if room_conflict(existing_class_sessions, class_session):
        return {'error': 'Room conflict'}, 400
    if teacher_conflict(existing_class_sessions, class_session):
        return {'error': 'Teacher conflict'}, 400
    if group_conflict(existing_class_sessions, class_session):
        return {'error': 'Group conflict'}, 400
    if semian_conflict(existing_class_sessions, class_session):
        return {'error': 'Semian conflict'}, 400
    return None, None


@class_session_bp.route('/class_sessions', methods=['GET'])
def get_all_class_sessions():
    year_id = request.args.get('year_id')

    class_sessions_query = ClassSession.query
    if year_id:
        class_sessions_query = class_sessions_query.join(Discipline).filter(Discipline.year_id == year_id)

    class_sessions = class_sessions_query.all()


    assert isinstance(class_sessions, list), "Expected list of class sessions"

    response = []
    n = len(class_sessions) 
    for i, cs in enumerate(class_sessions):

        assert (n - i) > 0, "Loop variant condition failed"

        discipline = db.session.get(Discipline, cs.discipline_id)
        teacher = db.session.get(Teacher, cs.teacher_id)
        room = db.session.get(Room, cs.room_id)
        time_slot = db.session.get(TimeSlot, cs.time_slot_id)

        assert discipline and teacher and room and time_slot, "Missing linked objects"
        assert cs.class_type in ["course", "seminar", "lab"], "Invalid class type"

        time_slot_str = f"{time_slot.start_time.strftime('%H:%M')} - {time_slot.end_time.strftime('%H:%M')}"
        response.append({
            'id': cs.id,
            'discipline': discipline.name,
            'teacher': teacher.name,
            'room': room.name,
            'day': time_slot.day,
            'time_slot': time_slot_str,
            'class_type': cs.class_type
        })


    assert all("id" in r and "discipline" in r for r in response), "Incomplete response format"
    return jsonify(response), 200


@class_session_bp.route('/class_session/<custom_id>', methods=['GET'])
def get_class_session(custom_id):

    try:
        id = int(custom_id)
    except ValueError:
        raise AssertionError("Invalid ID format")
    assert id > 0, "ID must be positive"

    class_session = db.session.get(ClassSession, id)
    if not class_session:
        return jsonify({'error': 'Class session not found'}), 404

    discipline = db.session.get(Discipline, class_session.discipline_id)
    teacher = db.session.get(Teacher, class_session.teacher_id)
    room = db.session.get(Room, class_session.room_id)
    time_slot = db.session.get(TimeSlot, class_session.time_slot_id)

    assert discipline and teacher and room and time_slot, "Missing related objects"

    response = {
        'id': class_session.id,
        'discipline': discipline.name,
        'teacher': teacher.name,
        'room': room.name,
        'time_slot': f"{time_slot.start_time.strftime('%H:%M')} - {time_slot.end_time.strftime('%H:%M')}",
        'class_type': class_session.class_type
    }

    assert "id" in response and "discipline" in response, "Invalid response format"

    return jsonify(response), 200


@class_session_bp.route('/add_class_session', methods=['POST'])
def add_class_session():
    data = request.get_json()

    required_fields = [
        'discipline_id', 'teacher_id', 'room_id', 'time_slot_id',
        'semian_id', 'group_id', 'class_type'
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

    discipline_id = data['discipline_id']
    teacher_id = data['teacher_id']
    room_id = data['room_id']
    time_slot_id = data['time_slot_id']
    semian_id = data['semian_id']
    group_id = data['group_id']
    class_type = data['class_type']

    discipline = db.session.get(Discipline, discipline_id)
    teacher = db.session.get(Teacher, teacher_id)
    room = db.session.get(Room, room_id)
    time_slot = db.session.get(TimeSlot, time_slot_id)
    semian = db.session.get(Semian, semian_id)
    group = db.session.get(Group, group_id)

    assert all([discipline, teacher, room, time_slot, semian, group]), "Invalid foreign key(s)"
    assert class_type in ["course", "seminar", "lab"], "Invalid class_type"

    if not match_room_class_type(room.room_type, class_type):
        return jsonify({'error': 'Room type does not match class type'}), 400

    new_class_session = ClassSession(
        discipline_id=discipline.id,
        teacher_id=teacher.id,
        room_id=room.id,
        time_slot_id=time_slot.id,
        semian_id=semian.id,
        group_id=group.id,
        class_type=class_type
    )
    
    new_class_session.discipline = discipline

    conflict_response, status_code = check_conflicts(ClassSession.query.all(), new_class_session)
    if conflict_response:
        return jsonify(conflict_response), status_code

    db.session.add(new_class_session)
    db.session.commit()

    assert new_class_session.id is not None, "Class session not saved"

    return jsonify({'message': 'Class session added successfully'}), 201

@class_session_bp.route('/edit_class_session/<custom_id>', methods=['PUT'])
def edit_class_session(custom_id):
    try:
        id = int(custom_id)
    except ValueError:
        raise AssertionError("Invalid ID format")
    assert id > 0, "ID must be positive"

    data = request.get_json()
    class_session = db.session.get(ClassSession, id)
    if not class_session:
        return jsonify({'error': 'Class session not found'}), 404

    assert isinstance(data, dict), "Request body must be JSON"

    class_session.discipline_id = data.get('discipline_id', class_session.discipline_id)
    class_session.teacher_id = data.get('teacher_id', class_session.teacher_id)
    class_session.room_id = data.get('room_id', class_session.room_id)
    class_session.time_slot_id = data.get('time_slot_id', class_session.time_slot_id)
    class_session.class_type = data.get('class_type', class_session.class_type)

    room = db.session.get(Room, class_session.room_id)
    time_slot = db.session.get(TimeSlot, class_session.time_slot_id)

    assert room and time_slot, "Room or TimeSlot missing"
    assert class_session.class_type in ["course", "seminar", "lab"], "Invalid class type"

    if not match_room_class_type(room.room_type, class_session.class_type):
        return jsonify({'error': 'Room type does not match class type'}), 400

    conflict_response, status_code = check_conflicts(ClassSession.query.all(), class_session)
    if conflict_response:
        return jsonify(conflict_response), status_code

    db.session.commit()

    assert class_session.id is not None, "Update failed"

    return jsonify({'message': 'Class session updated successfully'}), 200


@class_session_bp.route('/delete_class_session/<custom_id>', methods=['DELETE'])
def delete_class_session(custom_id):
    try:
        id = int(custom_id)
    except ValueError:
        raise AssertionError("Invalid ID format")
    assert id > 0, "ID must be positive"

    class_session = db.session.get(ClassSession, id)
    if not class_session:
        return jsonify({'error': 'Class session not found'}), 404

    db.session.delete(class_session)
    db.session.commit()

    assert db.session.get(ClassSession, id) is None, "Session deletion failed"

    return jsonify({'message': 'Class session deleted successfully'}), 200
