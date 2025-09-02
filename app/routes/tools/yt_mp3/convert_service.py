import os
import re
import yt_dlp
import time
import threading
from multiprocessing import Pool

# Dictionary to track job statuses
job_statuses = {}

def download_url(url, job_id):
    """Function that downloads a single URL."""
    try:
        # Clean URL (remove index parameter if it's present)
        url = re.sub(r'([&])index=\d+', '', url)

        # yt-dlp options for extracting MP3 audio
        flashdrive_dir = '/media/walson/music'
        if not os.path.exists(flashdrive_dir):
            print(f"Directory {flashdrive_dir} does not exist. Aborting download.")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(flashdrive_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'playlist_items': '1-',  # Download the entire playlist
        }

        # yt-dlp download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        job_statuses[job_id]["completed"] += 1
        time.sleep(0.5)  # Sleep for 500ms to reduce CPU load
    except Exception as e:
        job_statuses[job_id]["failed"].append(url)
        print(f"Error downloading {url}: {e}")


def download_mp3_to_flashdrive(urls, job_id):
    """Handles the batch processing of URLs in subprocesses."""
    if job_id not in job_statuses:
        job_statuses[job_id] = {
            "total": len(urls),
            "completed": 0,
            "failed": [],
            "status": "in-progress"
        }

    max_batch_size = 2
    num_batches = len(urls) // max_batch_size + (1 if len(urls) % max_batch_size > 0 else 0)

    # Create batches of URLs
    batches = [urls[i * max_batch_size: (i + 1) * max_batch_size] for i in range(num_batches)]

    # Process each batch of URLs in parallel using Pool
    for batch in batches:
        with Pool(processes=max_batch_size) as pool:
            pool.starmap(download_url, [(url, job_id) for url in batch])

    # After finishing, update job status
    job_statuses[job_id]["status"] = "completed"


def download_mp3_to_flashdrive_background(urls, job_id):
    """Run the download process in the background."""
    thread = threading.Thread(target=download_mp3_to_flashdrive, args=(urls, job_id))
    thread.daemon = True  # Daemon thread will exit when the main program exits
    thread.start()