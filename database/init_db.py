import sqlite3
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import config

def init_db():
    config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # Tabel Siswa
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        telegram_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT NOT NULL,
        class_name TEXT DEFAULT 'X TKJ',
        registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_active DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tabel Progres Materi Topik
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        topic_id INTEGER NOT NULL,
        is_completed INTEGER DEFAULT 0,
        video_watched INTEGER DEFAULT 0,
        completed_at DATETIME,
        UNIQUE(telegram_id, topic_id),
        FOREIGN KEY(telegram_id) REFERENCES students(telegram_id)
    )
    """)

    # Tabel Riwayat Kuis
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        topic_id INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        correct_answers INTEGER NOT NULL,
        final_score REAL NOT NULL,
        attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(telegram_id) REFERENCES students(telegram_id)
    )
    """)

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Database SQLite berhasil diinisialisasi di: {config.DATABASE_PATH}")

if __name__ == "__main__":
    init_db()
