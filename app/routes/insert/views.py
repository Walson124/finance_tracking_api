from flask import Blueprint, current_app, request

from app.routes.insert.get_data import get_data_service
from app.routes.insert.add_rows import add_rows_service
from app.routes.insert.get_income import get_income_service
from app.routes.insert.save_income import save_income_service
from app.routes.auth.views import require_auth

insert_bp = Blueprint('insert', __name__, url_prefix='/insert')


@insert_bp.route('/get_data', methods=['POST'])
@require_auth
def get_data():
    connector = current_app.config.get('connector')
    data = request.get_json()
    return get_data_service.run(connector, data)


@insert_bp.route('/add_rows', methods=['POST'])
@require_auth
def add_rows():
    connector = current_app.config.get('connector')
    data = request.get_json()
    return add_rows_service.run(connector, data)

@insert_bp.route('/get_income', methods=['GET'])
@require_auth
def get_income():
    connector = current_app.config.get('connector')
    return get_income_service.run(connector)

@insert_bp.route('/save_income', methods=['POST'])
@require_auth
def save_income():
    connector = current_app.config.get('connector')
    data = request.get_json()
    return save_income_service.save_income(connector, data)
