from Schoolmember import SchoolMember
from Helpers import studentsearch, view_all_students
from database import create_connection

class Teacher(SchoolMember):
    def __init__(self, full_name, id_number, department):
        super().__init__(full_name, id_number)
        self.position = "Teacher"
        self.department = department

    def studentlist(self):
        print(f"\nStudents ({self.department}  class):")
        for student in view_all_students():
            print(f"{student['id']} - {student['full_name']} - {student['grade']} - "
                  f"Score {student['score']} - Presence {student['presence']}%")
    
    def update_marks(self, student_id, score):
        student = studentsearch(student_id)
        if student:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE students SET score = ? WHERE id = ?", (score, student_id))
            connection.commit()
            connection.close()
            print(f"Updated score for {student['full_name']} to {score}.")
        else:
            print(f"No student found with ID {student_id}.")
    
    def update_attendance(self, student_id, presence):
        student = studentsearch(student_id)
        if student:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE students SET presence = ? WHERE id = ?", (presence, student_id))
            connection.commit()
            connection.close()
            print(f"Updated attendance for {student['full_name']} to {presence}%.")
        else:
            print(f"No student found with ID {student_id}.")
    
    def teacherlist(self):
        self.deny("list teachers")
    def register_student(self,*ignored):
        self.deny("register students")
    def remove_student(self,*ignored):
        self.deny("remove students")