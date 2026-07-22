import sqlite3
from security import hash_password

DB_NAME = 'schoolrecord.db'

DEFAULT_TEACHER_PASSWORD = "teach123"
DEFAULT_PRINCIPAL_PASSWORD = "principal123"
DEFAULT_ADMIN_PASSWORD = "admin123"


def create_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def _table_columns(cursor, table):
    cursor.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cursor.fetchall()]


def _add_column_if_missing(cursor, table, column, coltype):
    if column not in _table_columns(cursor, table):
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")


def initialize_database():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    grade TEXT,
                    score INTEGER DEFAULT 0,
                    presence INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    department TEXT,
                    pay INTEGER,
                    salt TEXT,
                    password_hash TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS principals (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    salt TEXT,
                    password_hash TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    salt TEXT,
                    password_hash TEXT
        )
    """)
    connection.commit()

    _add_column_if_missing(cursor, "teachers", "salt", "TEXT")
    _add_column_if_missing(cursor, "teachers", "password_hash", "TEXT")
    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        enter_students = [
            (1, "Sakeena Batool", "11-A", 95, 98),
            (2, "Abdul Samad", "11-B", 88, 92),
            (3, "Faaiz Khan", "11-C", 76, 85),
            (4, "Ahmed Raza", "11-A", 92, 97),
            (5, "Juwairiah Awais", "11-B", 84, 90),
            (6, "Haider Ali", "11-C", 79, 88),
            (7, "Azaan Zakir", "11-A", 91, 95),
            (8, "Ahsan Ali", "11-B", 87, 93),
            (9, "Muhammad Musab", "11-C", 82, 89),
            (10, "Zaafir Haidrie", "11-A", 98, 96),
            (11, "Zara Khan", "11-B", 85, 91),
            (12, "Malaika Subhani", "11-C", 78, 87),
            (13, "Hamza Saqib", "11-A", 93, 94),
            (14, "Murtaza Ali", "11-B", 89, 90),
            (15, "Abdullah Ehsan", "11-C", 81, 86),
        ]
        cursor.executemany(
            "INSERT INTO students (id, full_name, grade, score, presence) VALUES (?, ?, ?, ?, ?)",
            enter_students
        )

    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
        enter_teachers = [
            (2060, "Mr. Ahmed Maqsood", "Mathematics", 50000),
            (1920, "Mr. Rao Habib", "English", 48000),
            (4530, "Mr. Usama Virk ", "Computer Science", 52000),
            (7230, "Mr. Bari", "History & Geography", 63000),
            (1050, "Mr. Hamiz Javed", "Physics", 49000),
            (3090, "Mr. Hashim Ali", "Chemistry", 51000),
            (4120, "Mr. Taimoor Shakoori", "Biology", 47000),
        ]
        for teacher_id, full_name, department, pay in enter_teachers:
            salt, pwd_hash = hash_password(DEFAULT_TEACHER_PASSWORD)
            cursor.execute(
                "INSERT INTO teachers (id, full_name, department, pay, salt, password_hash) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (teacher_id, full_name, department, pay, salt, pwd_hash)
            )

    cursor.execute("SELECT id FROM teachers WHERE password_hash IS NULL OR salt IS NULL")
    rows_needing_password = cursor.fetchall()
    for row in rows_needing_password:
        salt, pwd_hash = hash_password(DEFAULT_TEACHER_PASSWORD)
        cursor.execute(
            "UPDATE teachers SET salt = ?, password_hash = ? WHERE id = ?",
            (salt, pwd_hash, row["id"])
        )

    cursor.execute("SELECT COUNT(*) FROM principals")
    if cursor.fetchone()[0] == 0:
        salt, pwd_hash = hash_password(DEFAULT_PRINCIPAL_PASSWORD)
        cursor.execute(
            "INSERT INTO principals (id, full_name, salt, password_hash) VALUES (?, ?, ?, ?)",
            (1010, "Mr. Shahzad", salt, pwd_hash)
        )

    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        salt, pwd_hash = hash_password(DEFAULT_ADMIN_PASSWORD)
        cursor.execute(
            "INSERT INTO admins (id, full_name, salt, password_hash) VALUES (?, ?, ?, ?)",
            (9010, "Head Admin", salt, pwd_hash)
        )

    connection.commit()
    connection.close()