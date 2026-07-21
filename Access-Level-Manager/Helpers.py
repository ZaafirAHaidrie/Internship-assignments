from database import create_connection

def studentsearch(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    connection.close()
    return dict(student) if student else None

def teachersearch(teacher_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teachers WHERE id = ?", (teacher_id,))
    teacher = cursor.fetchone()
    connection.close()
    return dict(teacher) if teacher else None

def principalsearch(principal_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM principals WHERE id = ?", (principal_id,))
    principal = cursor.fetchone()
    connection.close()
    return dict(principal) if principal else None

def adminsearch(admin_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admins WHERE id = ?", (admin_id,))
    admin = cursor.fetchone()
    connection.close()
    return dict(admin) if admin else None

def view_all_students():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    connection.close()
    return [dict(student) for student in students]

def view_all_teachers():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, full_name, department, pay FROM teachers")
    teachers = cursor.fetchall()
    connection.close()
    return [dict(teacher) for teacher in teachers]