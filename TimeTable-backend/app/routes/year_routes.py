from flask import Blueprint, jsonify, request 
from app.models import Year
years_bp = Blueprint('years', __name__)

@years_bp.route('/years', methods=['GET'])
def get_years():
    years = Year.query.all()
    return jsonify([year.to_dict() for year in years])

@years_bp.route('/year/<int:id>', methods=['GET'])
def get_year(id):
    year = Year.query.get(id)
    if not year:
        return {'error': 'Year not found'}, 404
    return {'id': year.id, 'name': year.name}, 200