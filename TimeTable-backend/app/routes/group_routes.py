from flask import Blueprint, jsonify, request 
from app.models import Group

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()

    assert isinstance(groups, list), "Expected list of groups"

    for g in groups:
        assert hasattr(g, 'id'), "Group missing id"
        assert hasattr(g, 'name'), "Group missing name"
        assert hasattr(g, 'year_id'), "Group missing year_id"
        assert hasattr(g, 'semian'), "Group missing semian"

    result = [group.to_dict() for group in groups]


    assert all("id" in g and "name" in g for g in result), "Invalid group structure"

    return jsonify(result)


@groups_bp.route('/group/<custom_id>', methods=['GET'])    
def get_group(custom_id):
    try:
        id = int(custom_id)
    except ValueError:
        raise AssertionError(f"Invalid group ID: not numeric → {custom_id}")
    assert id > 0, f"Invalid group ID: {id}"

    group = Group.query.get(id)
    if not group:
        return {'error': 'Group not found'}, 404

    assert group.name is not None, "Group missing name"
    assert group.year_id is not None, "Group missing year_id"
    assert group.semian is not None, "Group missing semian"

    result = {
        'id': group.id,
        'name': group.name,
        'year_id': group.year_id,
        'semian': group.semian.id if group.semian else None
    }

    assert 'id' in result and 'name' in result and 'year_id' in result and 'semian' in result, "Incomplete response data"

    return result, 200
