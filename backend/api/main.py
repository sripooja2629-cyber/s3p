"""
FastAPI Backend — NCERT Hinglish/Tanglish Chatbot
Main API entry point
"""
import os
import sys
import uuid
from typing import Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

from backend.db.models import create_tables, get_db, MistakeLog
from backend.rag.retriever import get_retriever
from backend.services.ollama_service import get_ollama
from backend.services.language_processor import (
    normalize_query, detect_language_style, check_out_of_syllabus_keywords
)
from backend.services.streak_tracker import (
    update_streak, log_question, check_repeated_topic, get_student_stats
)
from backend.services.analytics import get_teacher_dashboard_data
from backend.services.tts_service import generate_tts, get_tts_status
from backend.prompts.templates import SYSTEM_PROMPT

# ─── App Setup ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="NCERT Hinglish/Tanglish Chatbot API",
    description="AI study assistant for NCERT Class 9-10 students",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve TTS audio files
TTS_OUTPUT_DIR = os.getenv("TTS_OUTPUT_DIR", "./tts_output")
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)
app.mount("/audio", StaticFiles(directory=TTS_OUTPUT_DIR), name="audio")


# ─── Request/Response Models ──────────────────────────────────────────────────
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    generate_audio: bool = False


class MistakeRequest(BaseModel):
    session_id: Optional[str] = None
    topic: str
    question: str
    student_answer: str


class PracticeRequest(BaseModel):
    session_id: Optional[str] = None
    topic: str
    subject: Optional[str] = "general"
    class_level: Optional[str] = "9-10"


# ─── Startup ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    """Initialize DB tables on startup"""
    create_tables()
    print("🚀 NCERT Chatbot API started!")
    print(f"   Model: {os.getenv('OLLAMA_MODEL', 'llama3:8b')}")
    print(f"   Ollama URL: {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}")


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    ollama = get_ollama()
    retriever = get_retriever()
    tts_status = get_tts_status()

    return {
        "status": "ok",
        "ollama_running": ollama.check_health(),
        "rag_documents": retriever.get_stats()["total_documents"],
        "tts_available": tts_status,
        "model": os.getenv("OLLAMA_MODEL", "llama3:8b")
    }


# ─── Chat Endpoint ────────────────────────────────────────────────────────────
@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Main chat endpoint — handles student questions"""

    session_id = request.session_id or str(uuid.uuid4())
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    normalized_q, language_style, detected_subject = normalize_query(question)

    if check_out_of_syllabus_keywords(question):
        out_of_scope_response = get_out_of_scope_response(language_style)
        return {
            "session_id": session_id,
            "response": out_of_scope_response,
            "topic": "out_of_scope",
            "subject": "none",
            "language": language_style,
            "in_syllabus": False,
            "audio_url": None,
            "streak": None
        }

    ollama = get_ollama()
    topic_info = ollama.detect_topic(question)

    topic = "general"
    subject = detected_subject
    class_level = "9-10"
    in_syllabus = True

    if topic_info:
        topic = topic_info.get("topic", "general")
        subject = topic_info.get("subject", detected_subject)
        class_level = topic_info.get("class_level", "9-10")
        in_syllabus = topic_info.get("in_syllabus", True)

    if not in_syllabus:
        out_of_scope_response = get_out_of_scope_response(language_style)
        return {
            "session_id": session_id,
            "response": out_of_scope_response,
            "topic": topic,
            "subject": subject,
            "language": language_style,
            "in_syllabus": False,
            "audio_url": None,
            "streak": None
        }

    adaptive_mode = check_repeated_topic(db, session_id, topic, threshold=2)

    retriever = get_retriever()
    context = retriever.retrieve(question, n_results=3, subject_filter=subject)

    explanation = ollama.explain_concept(
        question=question,
        context=context,
        topic=topic,
        subject=subject,
        language_style=language_style,
        adaptive_mode=adaptive_mode,
        system_prompt_text=SYSTEM_PROMPT
    )

    streak_data = update_streak(db, session_id)
    log_question(
        db, session_id, question, topic, subject,
        class_level, language_style,
        was_repeated=adaptive_mode,
        difficulty_switched=adaptive_mode
    )

    audio_url = None
    if request.generate_audio:
        audio_path = generate_tts(explanation)
        if audio_path:
            filename = Path(audio_path).name
            audio_url = f"/audio/{filename}"

    return {
        "session_id": session_id,
        "response": explanation,
        "topic": topic,
        "subject": subject,
        "class_level": class_level,
        "language": language_style,
        "in_syllabus": True,
        "adaptive_mode": adaptive_mode,
        "audio_url": audio_url,
        "streak": streak_data
    }


# ─── Practice Questions ───────────────────────────────────────────────────────
@app.post("/practice")
async def generate_practice(request: PracticeRequest, db: Session = Depends(get_db)):
    session_id = request.session_id or str(uuid.uuid4())

    retriever = get_retriever()
    context = retriever.retrieve(request.topic, n_results=2, subject_filter=request.subject)

    ollama = get_ollama()
    questions = ollama.generate_practice_questions(
        topic=request.topic,
        subject=request.subject,
        class_level=request.class_level,
        context=context,
        system_prompt_text=SYSTEM_PROMPT
    )

    if not questions:
        questions = {
            "topic": request.topic,
            "questions": [
                {"level": "easy", "question": f"Define {request.topic} in your own words.", "answer": "See NCERT textbook", "hint": "Think about the basic definition"},
                {"level": "medium", "question": f"Explain the significance of {request.topic} with an example.", "answer": "See NCERT textbook", "hint": "Use a real-life example"},
                {"level": "hard", "question": f"How does {request.topic} relate to other concepts in this chapter?", "answer": "See NCERT textbook", "hint": "Think about connections"}
            ]
        }

    return {"session_id": session_id, "practice_questions": questions}


# ─── Mistake Analyzer ─────────────────────────────────────────────────────────
@app.post("/analyze-mistake")
async def analyze_mistake(request: MistakeRequest, db: Session = Depends(get_db)):
    session_id = request.session_id or str(uuid.uuid4())

    language_style = detect_language_style(request.student_answer + " " + request.question)

    retriever = get_retriever()
    context = retriever.retrieve(request.topic, n_results=2)

    ollama = get_ollama()
    analysis = ollama.analyze_mistake(
        topic=request.topic,
        question=request.question,
        student_answer=request.student_answer,
        context=context,
        language_style=language_style,
        system_prompt_text=SYSTEM_PROMPT
    )

    mistake = MistakeLog(
        session_id=session_id,
        topic=request.topic,
        question=request.question,
        student_answer=request.student_answer,
        ai_analysis=analysis
    )
    db.add(mistake)
    db.commit()

    return {
        "session_id": session_id,
        "analysis": analysis,
        "topic": request.topic,
        "language": language_style
    }


# ─── Concept Map ──────────────────────────────────────────────────────────────
@app.get("/concept-map/{topic}")
async def get_concept_map(topic: str, subject: str = "general"):
    ollama = get_ollama()
    concept_map = ollama.generate_concept_map(
        topic=topic,
        subject=subject,
        system_prompt_text=SYSTEM_PROMPT
    )

    if not concept_map:
        return {
            "central_concept": topic,
            "connections": [
                {"related_concept": "Related Concept 1", "relationship": "is part of", "description": "Connection description"},
            ]
        }

    return concept_map


# ─── Student Stats ────────────────────────────────────────────────────────────
@app.get("/student/{session_id}/stats")
async def get_stats(session_id: str, db: Session = Depends(get_db)):
    return get_student_stats(db, session_id)


# ─── Teacher Dashboard ────────────────────────────────────────────────────────
@app.get("/teacher/dashboard")
async def teacher_dashboard(db: Session = Depends(get_db)):
    return get_teacher_dashboard_data(db)


# ─── RAG Stats ───────────────────────────────────────────────────────────────
@app.get("/rag/stats")
async def rag_stats():
    retriever = get_retriever()
    return retriever.get_stats()


# ─── Helper ──────────────────────────────────────────────────────────────────
def get_out_of_scope_response(language_style: str) -> str:
    if language_style == "tanglish":
        return (
            "Ayyo da! Idhu NCERT Class 9-10 Science/Maths scope-la illa. "
            "Naan sirf NCERT Class 9-10 Science aur Maths paththi help panna mudiyum. "
            "Vera yethavadhu doubt irundha sollu! 😊"
        )
    else:
        return (
            "Yaar, yeh topic mera area nahi hai! 😅 "
            "Main sirf NCERT Class 9-10 Science aur Maths mein expert hoon. "
            "Is syllabus se related koi bhi doubt pooch — main pakka help karunga! 💪"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.api.main:app",
        host=os.getenv("FASTAPI_HOST", "0.0.0.0"),
        port=int(os.getenv("FASTAPI_PORT", 8000)),
        reload=True
    )
