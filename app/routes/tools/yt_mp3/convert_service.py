import os
import yt_dlp

def download_mp3_to_flashdrive(urls):
    # Flash drive mounted path (matches docker-compose volume mount)
    flashdrive_dir = '/media/walson/music'  # Correct path inside container
    os.makedirs(flashdrive_dir, exist_ok=True)  # Create the folder if it doesn't exist

    # yt-dlp options for extracting MP3 audio
    ydl_opts = {
        'format': 'bestaudio/best',  # Choose the best audio format
        'outtmpl': os.path.join(flashdrive_dir, '%(title)s.%(ext)s'),  # Save to flash drive with the title as filename
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Set quality to 192kbps
        }],
        'quiet': True,  # Suppress output
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Specify ffmpeg binary location
    }

    # Use yt-dlp to download each video as an MP3
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                ydl.download([url])
                print(f"Downloaded: {url}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")
