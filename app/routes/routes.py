import secrets
from flask import Blueprint, request, jsonify

main_bp = Blueprint('main', __name__)

from app.routes.home.views import home_bp
from app.routes.general.views import general_bp
from app.routes.insert.views import insert_bp
from app.routes.analysis.views import analysis_bp
from app.routes.goals.views import goals_bp
from app.routes.tools.views import tools_bp

main_bp.register_blueprint(home_bp)
main_bp.register_blueprint(general_bp)
main_bp.register_blueprint(insert_bp)
main_bp.register_blueprint(analysis_bp)
main_bp.register_blueprint(goals_bp)
main_bp.register_blueprint(tools_bp)

@main_bp.route('/')
def index():
    return "/"

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    # TODO: validate user/password (hash compare, DB, etc.)
    if email != "test@test.com" or password != "pass":
        return jsonify({"error": "Invalid credentials"}), 401

    session = secrets.token_urlsafe(32)
    # TODO: store session server-side (db/redis) or use JWT
    return jsonify({"session": session})
