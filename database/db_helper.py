import sqlite3
import datetime
from pathlib import Path
import config

def get_connection():
    return sqlite3.connect(config.DATABASE_PATH)

def register_student(telegram_id: int, username: str, full_name: str, class_name: str = "X TKJ"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO students (telegram_id, username, full_name, class_name, last_active)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(telegram_id) DO UPDATE SET
        username=excluded.username,
        full_name=excluded.full_name,
        last_active=CURRENT_TIMESTAMP
    """, (telegram_id, username, full_name, class_name))
    conn.commit()
    conn.close()

def mark_topic_completed(telegram_id: int, topic_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO topic_progress (telegram_id, topic_id, is_completed, completed_at)
    VALUES (?, ?, 1, CURRENT_TIMESTAMP)
    ON CONFLICT(telegram_id, topic_id) DO UPDATE SET
        is_completed=1,
        completed_at=CURRENT_TIMESTAMP
    """, (telegram_id, topic_id))
    conn.commit()
    conn.close()

def mark_video_watched(telegram_id: int, topic_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO topic_progress (telegram_id, topic_id, video_watched)
    VALUES (?, ?, 1)
    ON CONFLICT(telegram_id, topic_id) DO UPDATE SET
        video_watched=1
    """, (telegram_id, topic_id))
    conn.commit()
    conn.close()

def save_quiz_attempt(telegram_id: int, topic_id: int, total_q: int, correct: int, score: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO quiz_attempts (telegram_id, topic_id, total_questions, correct_answers, final_score)
    VALUES (?, ?, ?, ?, ?)
    """, (telegram_id, topic_id, total_q, correct, score))
    conn.commit()
    conn.close()

def get_student_stats(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ambil topik yang selesai
    cursor.execute("""
    SELECT topic_id FROM topic_progress WHERE telegram_id = ? AND is_completed = 1
    """, (telegram_id,))
    completed_topics = [row[0] for row in cursor.fetchall()]

    # Ambil rata-rata skor kuis
    cursor.execute("""
    SELECT AVG(final_score), COUNT(attempt_id) FROM quiz_attempts WHERE telegram_id = ?
    """, (telegram_id,))
    row = cursor.fetchone()
    avg_score = round(row[0], 1) if row and row[0] is not None else 0.0
    quiz_count = row[1] if row and row[1] is not None else 0

    conn.close()
    return {
        "completed_topics": completed_topics,
        "completed_count": len(completed_topics),
        "avg_score": avg_score,
        "quiz_count": quiz_count
    }
