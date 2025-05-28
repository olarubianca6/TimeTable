from flask import Blueprint, jsonify, request 
from app.models import Discipline

disciplines_bp = Blueprint('disciplines', __name__)


@disciplines_bp.route('/disciplines', methods=['GET'])  
def get_disciplines():
    disciplines = Discipline.query.all()

    assert isinstance(disciplines, list), "Expected list of disciplines"

    for d in disciplines:
 
        assert hasattr(d, 'id'), "Discipline missing id"
        assert hasattr(d, 'name'), "Discipline missing name"

    result = [discipline.to_dict() for discipline in disciplines]

    assert all("id" in d and "name" in d for d in result), "Invalid discipline structure"

    return jsonify(result)


@disciplines_bp.route('/discipline/<custom_id>', methods=['GET'])
def get_discipline(custom_id):

    try:
        id = int(custom_id)
    except ValueError:
        raise AssertionError(f"ID not numeric: {custom_id}")

    assert id > 0, f"Invalid discipline ID: {id}"

    discipline = Discipline.query.get(id)
    if not discipline:
        return {'error': 'Discipline not found'}, 404

    assert discipline.name is not None, "Discipline missing name"

    result = {'id': discipline.id, 'name': discipline.name}

    assert 'id' in result and 'name' in result, "Invalid response format"

    return result, 200
