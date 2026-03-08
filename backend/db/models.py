from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ncert_chatbot.db")
os.makedirs("./data", exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    streak_days = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    questions_today = Column(Integer, default=0)
    last_streak_date = Column(String(20), nullable=True)


class QuestionHistory(Base):
    __tablename__ = "question_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    question = Column(Text)
    topic = Column(String(200), nullable=True)
    subject = Column(String(50), nullable=True)
    class_level = Column(String(10), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    language_detected = Column(String(20), default="hinglish")
    was_repeated = Column(Boolean, default=False)
    difficulty_switched = Column(Boolean, default=False)


class TopicFrequency(Base):
    __tablename__ = "topic_frequency"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), index=True)
    subject = Column(String(50))
    ask_count = Column(Integer, default=1)
    last_asked = Column(DateTime, default=datetime.utcnow)
    week_start = Column(String(20))


class MistakeLog(Base):
    __tablename__ = "mistake_log"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    topic = Column(String(200))
    question = Column(Text)
    student_answer = Column(Text)
    correct_answer = Column(Text, nullable=True)
    ai_analysis = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    topic = Column(String(200))
    difficulty = Column(String(20))
    question_text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
