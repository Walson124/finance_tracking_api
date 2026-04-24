from flask import Blueprint, current_app, request

from app.routes.analysis.pi_chart import pi_chart_service
from app.routes.analysis.stack_chart import stack_chart_service
from app.routes.auth.views import require_auth

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_bp.route('/get_params', methods=['GET'])
@require_auth
def get_params():
    connector = current_app.config.get('connector')
    return pi_chart_service.get_params(connector)

@analysis_bp.route('/get_pi_chart', methods=['POST'])
@require_auth
def get_pi_chart():
    connector = current_app.config.get('connector')
    data = request.get_json()
    return pi_chart_service.get_data(connector, data)

@analysis_bp.route('/get_stack_chart', methods=['GET'])
@require_auth
def get_stack_chart():
    connector = current_app.config.get('connector')
    return stack_chart_service.get_data(connector)
