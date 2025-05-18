from flask import Blueprint, jsonify, request 
from app.models import  Discipline
disciplines_bp = Blueprint('disciplines', __name__)

@disciplines_bp.route('/disciplines', methods=['GET'])  
def get_disciplines():
    disciplines = Discipline.query.all()
    return jsonify([discipline.to_dict() for discipline in disciplines])

@disciplines_bp.route('/discipline/<int:id>', methods=['GET'])
def get_discipline(id):
    discipline = Discipline.query.get(id)
    if not discipline:
        return {'error': 'Discipline not found'}, 404
    return {'id': discipline.id, 'name': discipline.name}, 200