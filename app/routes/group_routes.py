from flask import Blueprint, jsonify, request 
from app.models import  Group
groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    return jsonify([group.to_dict() for group in groups])

@groups_bp.route('/group/<int:id>', methods=['GET'])    
def get_group(id):
    group = Group.query.get(id)
    if not group:
        return {'error': 'Group not found'}, 404
    return {'id': group.id, 'name': group.name}, 200