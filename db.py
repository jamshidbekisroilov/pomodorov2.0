import sqlite3
import os
import sys

# 📦 Fayl joylashuvi (PyInstaller uchun mos)
def get_db_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)  # ✅ .exe joylashgan papka
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "pomodoro.db")


def get_connection():
    return sqlite3.connect(get_db_path())

# 🏗️ Jadval yaratish
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            day TEXT NOT NULL,
            date TEXT NOT NULL,
            pomodoro_count INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completed_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            date TEXT NOT NULL,
            pomodoro_count INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS single_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            date TEXT NOT NULL,
            pomodoro_count INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()

# 💾 Saqlash funksiyalari
def save_weekly_task(task_name, day, date, pomodoro_count):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weekly_tasks (task_name, day, date, pomodoro_count)
        VALUES (?, ?, ?, ?)
    """, (task_name, day, date, pomodoro_count))
    conn.commit()
    conn.close()

def save_completed_task(task_name, date, pomodoro_count=1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO completed_tasks (task_name, date, pomodoro_count)
        VALUES (?, ?, ?)
    """, (task_name, date, pomodoro_count))
    conn.commit()
    conn.close()

def save_single_task(task_name, date, pomodoro_count=1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO single_tasks (task_name, date, pomodoro_count)
        VALUES (?, ?, ?)
    """, (task_name, date, pomodoro_count))
    conn.commit()
    conn.close()

# 📖 O‘qish funksiyalari
def get_today_weekly_tasks(today_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_name, pomodoro_count FROM weekly_tasks
        WHERE date = ?
    """, (today_date,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_all_weekly_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_name, day, date, pomodoro_count FROM weekly_tasks
        ORDER BY date ASC
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_completed_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_name, date, pomodoro_count FROM completed_tasks
        ORDER BY date DESC
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_all_single_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_name, date, pomodoro_count FROM single_tasks
        ORDER BY date DESC
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# 📊 Statistik tahlil
def get_task_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT task_name, SUM(pomodoro_count) FROM completed_tasks
        GROUP BY task_name
    """)
    completed = cursor.fetchall()

    cursor.execute("""
        SELECT task_name, SUM(pomodoro_count) FROM weekly_tasks
        GROUP BY task_name
    """)
    planned = cursor.fetchall()

    conn.close()
    return {"completed": completed, "planned": planned}
