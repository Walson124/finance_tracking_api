import secrets
from flask import Blueprint, request, jsonify

main_bp = Blueprint('main', __name__)

from app.routes.auth.views import auth_bp
from app.routes.home.views import home_bp
from app.routes.general.views import general_bp
from app.routes.insert.views import insert_bp
from app.routes.analysis.views import analysis_bp
from app.routes.goals.views import goals_bp
from app.routes.tools.views import tools_bp

main_bp.register_blueprint(auth_bp)
main_bp.register_blueprint(home_bp)
main_bp.register_blueprint(general_bp)
main_bp.register_blueprint(insert_bp)
main_bp.register_blueprint(analysis_bp)
main_bp.register_blueprint(goals_bp)
main_bp.register_blueprint(tools_bp)

@main_bp.route('/')
def index():
    return "/"
