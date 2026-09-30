from pathlib import Path
import sqlite3
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FOLDER = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_FOLDER / "mirror.db"


def get_connection():
    DATA_FOLDER.mkdir(exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            process TEXT NOT NULL,
            title TEXT,
            pid INTEGER
        )
    """)

    connection.commit()
    connection.close()


def save_activity(process, title, pid):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO activity (timestamp, process, title, pid)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().isoformat(timespec="seconds"),
        process,
        title,
        pid
    ))

    connection.commit()
    connection.close()


def get_recent_activity(limit=20):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT timestamp, process, title, pid
        FROM activity
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    connection.close()

    activities = []

    for timestamp, process, title, pid in rows:
        activities.append({
            "timestamp": timestamp,
            "process": process,
            "title": title,
            "pid": pid
        })

    return activities


if __name__ == "__main__":
    initialize_database()

    print("MIRROR database initialized at:")
    print(DATABASE_PATH)

    print("\nRecent activity:")
    print("----------------")

    activities = get_recent_activity()

    for activity in activities:
        print(
            f'{activity["timestamp"]} | '
            f'{activity["process"]} | '
            f'{activity["title"]}'
        )