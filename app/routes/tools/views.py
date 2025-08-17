from flask import Blueprint, current_app, request

from app.routes.tools.yt_mp3.views import yt_mp3_bp

tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

tools_bp.register_blueprint(yt_mp3_bp)

@tools_bp.route('/healthCheck', methods=['GET'])
def health_check():
    current_app.logger.info("Health check endpoint hit")
    return 'OK', 200
