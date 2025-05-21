from flask import Blueprint, jsonify, request
from app.models import TimeSlot

time_bp = Blueprint('time_slots', __name__)


@time_bp.route('/time_slots', methods=['GET'])
def get_all_time_slots():
    time_slots = TimeSlot.query.all()

    response = [
        {
            'id': slot.id,
            'day': slot.day,
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M')
        }
        for slot in time_slots
    ]

    return jsonify(response), 200
