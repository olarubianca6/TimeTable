
from flask import Blueprint, jsonify, request 
from app.models import  Student

students_bp = Blueprint('students', __name__)

@students_bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    
    assert isinstance(students, list), "Expected list of students"
    
    for student in students:
        assert hasattr(student, 'id'), "Student missing id"
        assert hasattr(student, 'name'), "Student missing name"
        
    return jsonify([student.to_dict() for student in students])

@students_bp.route('/student/<custom_id>', methods=['GET'])
def get_student(custom_id):
    
    assert custom_id.isdigit() and int(custom_id) > 0, f"Invalid student ID: {custom_id}"
    id = int(custom_id)
    student = Student.query.get(id)
    
    if not student:
        return {'error': 'Student not found'}, 404
    assert student.name is not None, "Student missing name"
    
    result = {'id': student.id, 'name': student.name}
    assert 'id' in result and 'name' in result, "Invalid response format"
    
    return result, 200

