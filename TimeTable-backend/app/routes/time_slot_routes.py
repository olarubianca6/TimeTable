from flask import Blueprint, jsonify, request
from app.models import TimeSlot

time_bp = Blueprint('time_slots', __name__)


@time_bp.route('/time_slots', methods=['GET'])
def get_all_time_slots():
    time_slots = TimeSlot.query.all()

    assert isinstance(time_slots, list), "Expected list of time slots"

    response = []
    for slot in time_slots:
        assert hasattr(slot, 'id'), "TimeSlot missing id"
        assert hasattr(slot, 'day'), "TimeSlot missing day"
        assert hasattr(slot, 'start_time'), "TimeSlot missing start_time"
        assert hasattr(slot, 'end_time'), "TimeSlot missing end_time"
        assert slot.start_time < slot.end_time, "Invalid time slot: start_time >= end_time"

        response.append({
            'id': slot.id,
            'day': slot.day,
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M')
        })
        
    assert len(response) == len(time_slots), "Mismatch in number of time slots returned"
    assert all('id' in s and 'day' in s and 'start_time' in s and 'end_time' in s for s in response), \
        "Invalid structure in time_slots response"

    return jsonify(response), 200
