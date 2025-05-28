from flask import Blueprint, jsonify, request 
from app.models import Room

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()

    assert isinstance(rooms, list), "Expected list of rooms"
    for r in rooms:

        assert hasattr(r, 'id'), "Room missing id"
        assert hasattr(r, 'name'), "Room missing name"

    return jsonify([room.to_dict() for room in rooms])


@rooms_bp.route('/room/<custom_id>', methods=['GET'])
def get_room(custom_id):
    try:
        id = int(custom_id)
    except ValueError:
        raise AssertionError(f"ID not numeric: {custom_id}")
    assert id > 0, f"Invalid room ID: {id}"

    room = Room.query.get(id)
    if not room:
        return {'error': 'Room not found'}, 404
    
    assert room.name is not None, "Room missing name"

    result = {'id': room.id, 'name': room.name}
    assert 'id' in result and 'name' in result, "Invalid response"

    return result, 200
