from Schoolmember import SchoolMember
from Helpers import studentsearch, teachersearch, view_all_students, view_all_teachers
from database import create_connection
from security import hash_password

STUDENT_FIELDS = {"full_name", "grade", "score", "presence"}
class Admin(SchoolMember):
    def __init__(self, full_name, id_number):
        super().__init__(full_name, id_number)
        self.position = "Admin"
    
    def studentlist(self):
        print("\nStudents (Admin view):")
        for student in view_all_students():
            print(student)
    
    def teacherlist(self):
        print("\nStaff (Admin view):")
        for teacher in view_all_teachers():
            print(teacher)
    
    def register_student(self,studentid, full_name, grade, score=0, presence=0):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
             "INSERT INTO students (id, full_name, grade, score, presence) VALUES (?, ?, ?, ?, ?)",
            (studentid, full_name, grade, score, presence)
        )
        connection.commit()
        connection.close()
        print(f"Registered student {full_name} with ID {studentid}")
    
    def modify_student(self, studentid, field, value):
        student = studentsearch(studentid)
        if student and field in STUDENT_FIELDS:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute(f"UPDATE students SET {field} = ? WHERE id = ?", (value, studentid))
            connection.commit()
            connection.close()
            print(f"Updated {field} for {student['full_name']} to {value}")
        else:
            print(f"Update failed")
        
    def remove_student(self,studentid):
        student = studentsearch(studentid)
        if student:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (studentid,))
            connection.commit()
            connection.close()
            print(f"Removed student {student['full_name']} with ID {studentid}")
        else:
            print(f"Removal Failed")

    def register_teacher(self, teacherid, full_name, department, pay, password):
        salt, password_hash = hash_password(password)
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO teachers (id, full_name, department, pay, salt, password_hash) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (teacherid, full_name, department, pay, salt, password_hash)
        )
        connection.commit()
        connection.close()
        print(f"Registered teacher {full_name} with ID {teacherid}")

    def set_pay(self, teacherid, pay):
        teacher = teachersearch(teacherid)
        if teacher:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE teachers SET pay = ? WHERE id = ?", (pay, teacherid))
            connection.commit()
            connection.close()
            print(f"Updated pay for {teacher['full_name']} to {pay}")
        else:
            print("Update failed")
    
    def remove_teacher(self, teacherid):
        teacher = teachersearch(teacherid)
        if teacher:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM teachers WHERE id = ?", (teacherid,))
            connection.commit()
            connection.close()
            print(f"Removed teacher {teacher['full_name']} with ID {teacherid}")
        else:
            print("Removal failed")