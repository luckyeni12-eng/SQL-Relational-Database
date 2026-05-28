# Student Performance Tracker
# Demonstrates SQL Relational Database concepts using SQLite
# Includes CRUD operations, joins, aggregates, and date filtering

import sqlite3
from datetime import datetime


# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def connect_db():
    """Create and return database connection"""
    conn = sqlite3.connect("school.db")
    return conn


# -------------------------------
# DATABASE SETUP
# -------------------------------
def setup_database():
    """Create tables for students and grades"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            score INTEGER,
            created_at TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# INSERT OPERATIONS (CREATE)
# -------------------------------
def add_student(name, email):
    """Insert a new student safely (prevents duplicate crash)"""
    conn = connect_db()
    cursor = conn.cursor()

    # ✔️ FIX: check if email already exists
    cursor.execute("SELECT id FROM students WHERE email = ?", (email,))
    existing = cursor.fetchone()

    if existing:
        print(f"⚠️ Student with email '{email}' already exists. Skipping insert.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO students (name, email, created_at)
        VALUES (?, ?, ?)
    """, (name, email, datetime.now()))

    conn.commit()
    conn.close()


def add_grade(student_id, subject, score):
    """Insert a grade for a student"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO grades (student_id, subject, score, created_at)
        VALUES (?, ?, ?, ?)
    """, (student_id, subject, score, datetime.now()))

    conn.commit()
    conn.close()


# -------------------------------
# READ OPERATIONS
# -------------------------------
def get_all_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_student_report():
    """JOIN students and grades tables"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.name, grades.subject, grades.score
        FROM students
        JOIN grades ON students.id = grades.student_id
    """)

    results = cursor.fetchall()
    conn.close()
    return results


# -------------------------------
# UPDATE OPERATION
# -------------------------------
def update_grade(grade_id, new_score):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE grades
        SET score = ?
        WHERE id = ?
    """, (new_score, grade_id))

    conn.commit()
    conn.close()


# -------------------------------
# DELETE OPERATION
# -------------------------------
def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    conn.commit()
    conn.close()


# -------------------------------
# AGGREGATE FUNCTIONS
# -------------------------------
def get_statistics():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(score) FROM grades")
    avg_score = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM grades")
    total_grades = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(score) FROM grades")
    total_score = cursor.fetchone()[0]

    conn.close()

    return {
        "average": avg_score,
        "count": total_grades,
        "sum": total_score
    }


# -------------------------------
# DATE FILTERING
# -------------------------------
def get_recent_grades():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM grades
        WHERE created_at >= datetime('now', '-1 day')
    """)

    results = cursor.fetchall()
    conn.close()
    return results


# -------------------------------
# MAIN PROGRAM DEMO
# -------------------------------
def main():
    setup_database()

    # Sample data (safe to rerun now)
    add_student("John Doe", "john@example.com")
    add_student("Jane Smith", "jane@example.com")

    add_grade(1, "Math", 85)
    add_grade(1, "Science", 90)
    add_grade(2, "Math", 78)

    print("\nALL STUDENTS:")
    for s in get_all_students():
        print(s)

    print("\nSTUDENT REPORT (JOIN):")
    for r in get_student_report():
        print(r)

    print("\nSTATISTICS:")
    print(get_statistics())

    print("\nRECENT GRADES:")
    for g in get_recent_grades():
        print(g)

    update_grade(1, 95)
    delete_student(2)


if __name__ == "__main__":
    main()