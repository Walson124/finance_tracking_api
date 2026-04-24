from flask import Blueprint, current_app, request

from app.routes.general.get_users import get_users_service
from app.routes.auth.views import require_auth

general_bp = Blueprint('general', __name__, url_prefix='/general')


@general_bp.route('/get_users', methods=['GET'])
@require_auth
def get_users():
    connector = current_app.config.get('connector')
    return get_users_service.run(connector)
