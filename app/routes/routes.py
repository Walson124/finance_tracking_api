from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.routes.general.views import general_bp
from app.routes.insert.views import insert_bp
from app.routes.analysis.views import analysis_bp

main_bp.register_blueprint(general_bp)
main_bp.register_blueprint(insert_bp)
main_bp.register_blueprint(analysis_bp)

@main_bp.route('/')
def index():
    return "/"