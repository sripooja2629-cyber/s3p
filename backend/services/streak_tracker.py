from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from backend.db.models import Student, QuestionHistory, TopicFrequency


def get_or_create_student(db: Session, session_id: str) -> Student:
    student = db.query(Student).filter(Student.session_id == session_id).first()
    if not student:
        student = Student(session_id=session_id)
        db.add(student)
        db.commit()
        db.refresh(student)
    return student


def update_streak(db: Session, session_id: str) -> dict:
    student = get_or_create_student(db, session_id)
    today_str = date.today().isoformat()
    student.total_questions += 1
    student.last_active = datetime.utcnow()
    if student.last_streak_date != today_str:
        student.questions_today = 1
        student.last_streak_date = today_str
    else:
        student.questions_today += 1
    if student.questions_today == 3:
        student.streak_days += 1
    db.commit()
    db.refresh(student)
    return {
        "streak_days": student.streak_days,
        "questions_today": student.questions_today,
        "total_questions": student.total_questions,
        "streak_earned_today": student.questions_today >= 3,
        "questions_needed_for_streak": max(0, 3 - student.questions_today),
        "milestone": get_milestone(student.streak_days)
    }


def get_milestone(streak_days: int) -> str:
    if streak_days >= 30: return "🏆 Legend! 30-day streak!"
    elif streak_days >= 14: return "🔥 Super Star! 2-week streak!"
    elif streak_days >= 7: return "⭐ Week Champion!"
    elif streak_days >= 3: return "💪 On a Roll!"
    elif streak_days >= 1: return "🌱 Getting Started!"
    return ""


def log_question(db: Session, session_id, question, topic, subject,
                 class_level, language, was_repeated=False, difficulty_switched=False):
    db.add(QuestionHistory(
        session_id=session_id, question=question, topic=topic, subject=subject,
        class_level=class_level, language_detected=language,
        was_repeated=was_repeated, difficulty_switched=difficulty_switched
    ))
    db.commit()
    update_topic_frequency(db, topic, subject)


def update_topic_frequency(db: Session, topic: str, subject: str):
    week_start = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    existing = db.query(TopicFrequency).filter(
        TopicFrequency.topic == topic, TopicFrequency.week_start == week_start
    ).first()
    if existing:
        existing.ask_count += 1
        existing.last_asked = datetime.utcnow()
    else:
        db.add(TopicFrequency(topic=topic, subject=subject, ask_count=1, week_start=week_start))
    db.commit()


def check_repeated_topic(db: Session, session_id: str, topic: str, threshold: int = 2) -> bool:
    count = db.query(QuestionHistory).filter(
        QuestionHistory.session_id == session_id,
        QuestionHistory.topic == topic
    ).count()
    return count >= threshold


def get_student_stats(db: Session, session_id: str) -> dict:
    student = get_or_create_student(db, session_id)
    recent = db.query(QuestionHistory).filter(
        QuestionHistory.session_id == session_id
    ).order_by(QuestionHistory.timestamp.desc()).limit(10).all()
    recent_topics = list(set([q.topic for q in recent if q.topic]))[:5]
    return {
        "streak_days": student.streak_days,
        "questions_today": student.questions_today,
        "total_questions": student.total_questions,
        "recent_topics": recent_topics,
        "milestone": get_milestone(student.streak_days),
        "questions_needed": max(0, 3 - student.questions_today)
    }
