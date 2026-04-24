import json
import os
import re
import threading
import time

import yt_dlp

STATUS_FILE = '/tmp/yt_mp3_job_statuses.json'
_lock = threading.Lock()

MUSIC_DIR = os.getenv('MUSIC_DIR', '/media/walson/music')


def _read_statuses():
    try:
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write_statuses(statuses):
    with open(STATUS_FILE, 'w') as f:
        json.dump(statuses, f)


def _update_status(job_id, patch):
    with _lock:
        statuses = _read_statuses()
        if job_id in statuses:
            statuses[job_id].update(patch)
        _write_statuses(statuses)


def job_statuses(job_id=None):
    statuses = _read_statuses()
    if job_id is not None:
        return statuses.get(job_id)
    return statuses


def download_url(url, job_id):
    try:
        url = re.sub(r'([&])index=\d+', '', url)
        if not os.path.exists(MUSIC_DIR):
            print(f"Music directory {MUSIC_DIR} does not exist. Aborting.")
            _update_status(job_id, {"failed": _read_statuses().get(job_id, {}).get("failed", []) + [url]})
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(MUSIC_DIR, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'playlist_items': '1-',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with _lock:
            statuses = _read_statuses()
            if job_id in statuses:
                statuses[job_id]["completed"] += 1
            _write_statuses(statuses)

        time.sleep(0.5)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        with _lock:
            statuses = _read_statuses()
            if job_id in statuses:
                statuses[job_id]["failed"].append(url)
            _write_statuses(statuses)


def _run_downloads(urls, job_id):
    for url in urls:
        download_url(url, job_id)
    _update_status(job_id, {"status": "completed"})


def download_mp3_to_flashdrive_background(urls, job_id):
    with _lock:
        statuses = _read_statuses()
        statuses[job_id] = {"total": len(urls), "completed": 0, "failed": [], "status": "in-progress"}
        _write_statuses(statuses)

    thread = threading.Thread(target=_run_downloads, args=(urls, job_id), daemon=True)
    thread.start()
