from flask import Blueprint, jsonify, request 
from app.models import  Teacher
teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    
    assert isinstance(teachers, list), "Expected list of teachers"
    
    for teacher in teachers:
        assert hasattr(teacher, 'id'), "Teacher missing id"
        assert hasattr(teacher, 'name'), "Teacher missing name"
        
    return jsonify([teacher.to_dict() for teacher in teachers])

@teachers_bp.route('/teacher/<custom_id>', methods=['GET'])
def get_teacher(custom_id):
    
    assert custom_id.isdigit() and int(custom_id) > 0, f"Invalid teacher ID: {custom_id}"
    
    id = int(custom_id)
    teacher = Teacher.query.get(id)
    
    if not teacher:
        return {'error': 'Teacher not found'}, 404
    
    assert teacher.name is not None, "Teacher missing name"
    
    result = {'id': teacher.id, 'name': teacher.name}
    assert 'id' in result and 'name' in result, "Invalid response format"
    
    return result, 200
