#!/bin/bash
# NCERT Chatbot — Quick Start Script
set -e

echo ""
echo "📚 NCERT Hinglish/Tanglish Study Buddy"
echo "======================================="
echo ""

if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Install from: https://ollama.ai"
    exit 1
fi

echo "🤖 Checking Ollama model..."
if ! ollama list | grep -q "llama3:8b"; then
    echo "📥 Pulling llama3:8b (this takes a few minutes on first run)..."
    ollama pull llama3:8b
else
    echo "✅ llama3:8b model found"
fi

if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🚀 Starting Ollama server..."
    ollama serve &
    sleep 3
fi
echo "✅ Ollama running"

echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt -q

CHROMA_PATH="./data/chroma_db"
if [ ! -d "$CHROMA_PATH" ] || [ -z "$(ls -A $CHROMA_PATH 2>/dev/null)" ]; then
    echo "📚 Ingesting NCERT content into ChromaDB..."
    python scripts/ingest_ncert.py
else
    echo "✅ NCERT content already ingested"
fi

echo ""
echo "⚡ Starting FastAPI backend on http://localhost:8000..."
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload &
FASTAPI_PID=$!
sleep 3

echo ""
echo "🎨 Starting Streamlit UI on http://localhost:8501..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  App ready at: http://localhost:8501"
echo "  API docs at:  http://localhost:8000/docs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

streamlit run frontend/app.py --server.port 8501

kill $FASTAPI_PID 2>/dev/null || true
