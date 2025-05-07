from flask import Blueprint, jsonify, request 
from app.models import  Room
rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])

@rooms_bp.route('/room/<int:id>', methods=['GET'])
def get_room(id):
    room = Room.query.get(id)
    if not room:
        return {'error': 'Room not found'}, 404
    return {'id': room.id, 'name': room.name}, 200