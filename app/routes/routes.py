from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.routes.insert.views import insert_bp
main_bp.register_blueprint(insert_bp)

@main_bp.route('/')
def index():
    return "/"