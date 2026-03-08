from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.models import TopicFrequency, QuestionHistory, Student


def get_top_topics_last_7_days(db: Session, limit: int = 10) -> list:
    week_ago = date.today() - timedelta(days=7)
    results = (
        db.query(QuestionHistory.topic, QuestionHistory.subject,
                 func.count(QuestionHistory.id).label("count"))
        .filter(QuestionHistory.timestamp >= week_ago, QuestionHistory.topic.isnot(None))
        .group_by(QuestionHistory.topic, QuestionHistory.subject)
        .order_by(func.count(QuestionHistory.id).desc()).limit(limit).all()
    )
    return [{"topic": r.topic, "subject": r.subject, "ask_count": r.count} for r in results]


def get_total_interactions(db: Session) -> dict:
    total = db.query(func.count(QuestionHistory.id)).scalar() or 0
    today_count = db.query(func.count(QuestionHistory.id)).filter(
        func.date(QuestionHistory.timestamp) == date.today()).scalar() or 0
    week_count = db.query(func.count(QuestionHistory.id)).filter(
        QuestionHistory.timestamp >= date.today() - timedelta(days=7)).scalar() or 0
    unique = db.query(func.count(func.distinct(QuestionHistory.session_id))).scalar() or 0
    return {"total_interactions": total, "today": today_count, "this_week": week_count, "unique_students": unique}


def get_subject_distribution(db: Session) -> list:
    results = (
        db.query(QuestionHistory.subject, func.count(QuestionHistory.id).label("count"))
        .filter(QuestionHistory.subject.isnot(None))
        .group_by(QuestionHistory.subject).order_by(func.count(QuestionHistory.id).desc()).all()
    )
    return [{"subject": r.subject, "count": r.count} for r in results]


def get_difficulty_trends(db: Session) -> list:
    results = (
        db.query(QuestionHistory.topic, func.count(QuestionHistory.id).label("total_asks"),
                 func.sum(func.cast(QuestionHistory.was_repeated, int)).label("repeat_count"))
        .filter(QuestionHistory.topic.isnot(None))
        .group_by(QuestionHistory.topic)
        .having(func.count(QuestionHistory.id) >= 2)
        .order_by(func.count(QuestionHistory.id).desc()).limit(15).all()
    )
    trends = []
    for r in results:
        repeat_rate = (r.repeat_count or 0) / max(r.total_asks, 1) * 100
        difficulty = "High" if repeat_rate > 50 else "Medium" if repeat_rate > 20 else "Low"
        trends.append({"topic": r.topic, "total_asks": r.total_asks,
                       "repeat_rate": round(repeat_rate, 1), "difficulty_level": difficulty})
    return trends


def get_daily_activity(db: Session, days: int = 7) -> list:
    activity = []
    for i in range(days - 1, -1, -1):
        day = date.today() - timedelta(days=i)
        count = db.query(func.count(QuestionHistory.id)).filter(
            func.date(QuestionHistory.timestamp) == day).scalar() or 0
        activity.append({"date": day.strftime("%d %b"), "questions": count})
    return activity


def get_teacher_dashboard_data(db: Session) -> dict:
    return {
        "top_topics": get_top_topics_last_7_days(db),
        "interactions": get_total_interactions(db),
        "subject_distribution": get_subject_distribution(db),
        "difficulty_trends": get_difficulty_trends(db),
        "daily_activity": get_daily_activity(db),
        "generated_at": datetime.utcnow().isoformat()
    }
