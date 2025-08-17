# finance_tracking_api

Backend service for the finance_app project.

## Features

- REST API for finance data analysis and conversion
- Endpoints for category, user, month, and year-based queries
- YouTube to MP3 conversion (writes to mounted flash drive)
- Designed to work with the frontend (`finance_tracking`) and Docker Compose

## Getting Started

**Local Development:**
```sh
python -m app.main
```
Run this command in the `finance_tracking_api` directory.

**Production (Docker):**
This service is orchestrated via Docker Compose in the main `finance_app` repo.

## API Endpoints

- `/tools/yt_mp3/convert` — Convert YouTube URLs to MP3 and save to flash drive
- `/analysis/get_params` — Get available years, months, categories, users
- `/analysis/get_pi_chart` — Get pie chart data for selected filters

## Environment

- Uses `.env` file for configuration (see `docker-compose.yml`)
- Flash drive is mounted to `/media/walson/music` inside the container

## Notes

- Ensure ffmpeg is installed (handled in Dockerfile)
- For local file output, check `/media/walson/music` (container) or `/media/walson/WALSON 15GB/music` (host)
- Designed to be used with the frontend and PostgreSQL database