# 📚 NCERT Hinglish/Tanglish AI Study Buddy

> **AI-01 | Hackathon 2025 — Frontier Edition**
> A doubt-clearing chatbot for NCERT Class 9–10 students that speaks the way India's real students think — in Hinglish and Tanglish.

---

## 🎯 What Is This?

India's 250 million school students think and communicate in code-mixed languages — Hinglish (Hindi+English) and Tanglish (Tamil+English). But every AI study tool responds in formal textbook English.

This project is a **fully local, open-source AI study assistant** that:

- ✅ Accepts Hinglish/Tanglish questions naturally
- ✅ Explains NCERT concepts like a helpful senior student
- ✅ Uses Indian real-life examples (cricket, dal-chawal, auto-rickshaw)
- ✅ Generates practice questions (Easy / Medium / Hard)
- ✅ Analyzes student mistakes from exams
- ✅ Shows concept maps connecting related topics
- ✅ Adapts to simpler analogies when students are confused
- ✅ Tracks daily streaks to gamify learning
- ✅ Voice explanations via TTS
- ✅ Teacher analytics dashboard

---

## 🚀 Quick Setup (Local)

### Step 1 — Install Ollama
```bash
# Windows: Download from https://ollama.ai/download
# Linux/macOS:
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2 — Pull Llama3 Model
```bash
ollama pull llama3:8b
# Downloads ~4.7GB — takes 5-10 mins on first run
```

### Step 3 — Setup Project
```bash
cd ncert_chatbot
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/ingest_ncert.py
```

### Step 4 — Run
```bash
# Terminal 1 — Backend
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
streamlit run frontend/app.py --server.port 8501
```

Open **http://localhost:8501** in your browser.

---

## 🐳 Docker Deployment

> Ollama must run on the host machine first.

```bash
# Start Ollama on host
ollama serve

# Build and start Docker containers
docker-compose up --build

# Access: http://localhost:8501
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System health check |
| POST | `/chat` | Main chat endpoint |
| POST | `/practice` | Generate 3 practice questions |
| POST | `/analyze-mistake` | Analyze student's wrong answer |
| GET | `/concept-map/{topic}` | Generate concept map |
| GET | `/student/{session_id}/stats` | Student streak & stats |
| GET | `/teacher/dashboard` | Teacher analytics |
| GET | `/rag/stats` | RAG database statistics |

---

## 💬 Example Interactions

**Hinglish:**
> "bhai Newton ka third law kya hai? samajh nahi aaya"

**Bot:**
> "Yaar, seedha example se samjhata hoon! Jab tu cricket ball throw karta hai — ball forward jaati hai, aur tera haath thoda peeche dhakka mehsoos karta hai? That's Newton's Third Law! 🚀"

**Tanglish:**
> "da, photosynthesis epdi nadakkuthu sollu"

**Bot:**
> "Dei, simple a explain panren! Tree oru chef maari — Sunlight = flame, CO₂ + water = ingredients, glucose = food! 🌱"

---

## ⚙️ System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| Storage | 10 GB | 20 GB |
| OS | Windows WSL2 / Linux / macOS | Ubuntu 22.04 |
| Python | 3.10+ | 3.11 |

---

## 📋 Troubleshooting

| Problem | Solution |
|---------|----------|
| Ollama not running | Run `ollama serve` in a separate terminal |
| Model not found | Run `ollama pull llama3:8b` |
| No NCERT content | Run `python scripts/ingest_ncert.py` |
| Slow responses | Normal on CPU — 30-60 seconds per response |
| TTS not working | `pip install gtts` |
| Port 8000 in use | Change `FASTAPI_PORT` in `.env` |

---

**Built for Hackathon 2025 — Frontier Edition | IEEE/AIC/SIH Aligned**
