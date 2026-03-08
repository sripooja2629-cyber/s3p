FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl supervisor && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data/chroma_db tts_output

RUN python scripts/ingest_ncert.py || echo "Ingest skipped"

RUN echo '[supervisord]\nnodaemon=true\nlogfile=/dev/stdout\nlogfile_maxbytes=0\n\n[program:backend]\ncommand=uvicorn backend.api.main:app --host 0.0.0.0 --port 8000\ndirectory=/app\nautostart=true\nautorestart=true\nstdout_logfile=/dev/stdout\nstdout_logfile_maxbytes=0\nstderr_logfile=/dev/stderr\nstderr_logfile_maxbytes=0\n\n[program:frontend]\ncommand=streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true\ndirectory=/app\nautostart=true\nautorestart=true\nstdout_logfile=/dev/stdout\nstdout_logfile_maxbytes=0\nstderr_logfile=/dev/stderr\nstderr_logfile_maxbytes=0\nenvironment=FASTAPI_URL="http://localhost:8000"' > /etc/supervisor/conf.d/app.conf

EXPOSE 8501

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/app.conf"]
