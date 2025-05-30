from flask import Blueprint, current_app, request

from app.routes.analysis.pi_chart import pi_chart_service

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_bp.route('/get_params', methods=['GET'])
def get_params():
    connector = current_app.config.get('connector')
    return pi_chart_service.get_params(
        connector
    )

@analysis_bp.route('/get_pi_chart', methods=['POST'])
def get_pi_chart():
    connector = current_app.config.get('connector')
    data = request.get_json()
    return pi_chart_service.get_data(
        connector,
        data
    )
