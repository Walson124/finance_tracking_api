from flask import Blueprint, current_app, request

from app.routes.home.get_data import get_data_service

home_bp = Blueprint('home', __name__, url_prefix='/home')

@home_bp.route('/get_data', methods=['POST'])
def get_data():
    connector = current_app.config.get('connector')
    data = request.get_json()
    return get_data_service.run(
        connector,
        data
    )