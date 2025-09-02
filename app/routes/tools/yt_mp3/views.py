from flask import Blueprint, request, jsonify, current_app
from .convert_service import download_mp3_to_flashdrive_background, job_statuses

yt_mp3_bp = Blueprint('yt_mp3', __name__, url_prefix='/yt_mp3')

@yt_mp3_bp.route('/convert', methods=['POST'])
def convert_youtube_to_mp3_view():
    urls = request.json.get('urls', [])
    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    # Generate a job ID and start the download process in the background
    job_id = str(hash(frozenset(urls)))
    
    # Start the download in the background
    download_mp3_to_flashdrive_background(urls, job_id)

    return jsonify({"message": "Download started", "job_id": job_id}), 200


@yt_mp3_bp.route('/status/<job_id>', methods=['GET'])
def check_job_status(job_id):
    """Endpoint to check the status of a job."""
    if job_id not in job_statuses:
        return {"error": "Job not found"}, 404
    
    status = job_statuses[job_id]
    return jsonify(status), 200
