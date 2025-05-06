from flask import Blueprint, jsonify, request 
from app.models import  Teacher
teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([teacher.to_dict() for teacher in teachers])

@teachers_bp.route('/teacher/<int:id>', methods=['GET'])
def get_teacher(id):
    teacher = Teacher.query.get(id)
    if not teacher:
        return {'error': 'Teacher not found'}, 404
    return {'id': teacher.id, 'name': teacher.name}, 200
