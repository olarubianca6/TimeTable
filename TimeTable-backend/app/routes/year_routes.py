from flask import Blueprint, jsonify, request 
from app.models import Year

years_bp = Blueprint('years', __name__)


@years_bp.route('/years', methods=['GET'])
def get_years():
    years = Year.query.all()
    
    assert isinstance(years, list), "Expected list of years"

    for y in years:
        assert hasattr(y, 'id'), "Missing id field in Year"
        assert hasattr(y, 'name'), "Missing name field in Year"

    return jsonify([year.to_dict() for year in years])


@years_bp.route('/year/<custom_id>', methods=['GET'])
def get_year(custom_id):

    assert custom_id.isdigit() and int(custom_id) > 0, f"Invalid year ID: {custom_id}"
    
    id = int(custom_id)
    year = Year.query.get(id)

    if not year:
        return {'error': 'Year not found'}, 404

    assert year.name is not None, "Year missing name"

    result = {'id': year.id, 'name': year.name}
    assert 'id' in result and 'name' in result, "Invalid response format"

    return result, 200
