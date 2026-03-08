FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential libsndfile1 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create data directories
RUN mkdir -p data/chroma_db tts_output

# Ingest NCERT content at build time
RUN python scripts/ingest_ncert.py

EXPOSE 8000 8501
