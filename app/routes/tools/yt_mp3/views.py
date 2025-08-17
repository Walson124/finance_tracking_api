from flask import Blueprint, request, jsonify, send_file, current_app
from .convert_service import download_mp3_to_flashdrive

yt_mp3_bp = Blueprint('yt_mp3', __name__, url_prefix='/yt_mp3')

@yt_mp3_bp.route('/convert', methods=['POST'])
def convert_youtube_to_mp3_view():
    urls = request.json.get('urls', [])
    if not urls:
        return {"error": "No URLs provided"}, 400

    # Download the MP3s to the flash drive
    download_mp3_to_flashdrive(urls)

    return {"message": "Download completed successfully"}, 200
   
@yt_mp3_bp.route('/healthCheck', methods=['GET'])
def health_check():
    current_app.logger.info("Health check endpoint hit")
    return 'OK', 200
