
from flask import Blueprint, jsonify, request 
from app.models import  Student
students_bp = Blueprint('students', __name__)

@students_bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@students_bp.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return {'error': 'Student not found'}, 404
    return {'id': student.id, 'name': student.name}, 200

