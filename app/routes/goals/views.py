from flask import Blueprint, current_app, request

from app.routes.goals.get_data import get_data_service

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route('/get_data', methods=['POST'])
def get_data():
    connector = current_app.config.get('connector')
    data = request.get_json()
    return get_data_service.run(
        connector,
        data
    )