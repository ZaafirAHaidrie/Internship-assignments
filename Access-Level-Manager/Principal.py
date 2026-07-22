from Schoolmember import SchoolMember
from Helpers import view_all_students, view_all_teachers

class Principal(SchoolMember):
    def __init__(self,full_name,id_number):
        super().__init__(full_name, id_number)
        self.position = "Principal"
    
    def studentlist(self):
        print("\nStudents (Principal view):")
        for student in view_all_students():
            print(f"{student['id']} - {student['full_name']} - {student['grade']} - "
                  f"Score {student['score']} - Presence {student['presence']}%")
    
    def teacherlist(self):
        print("\nTeachers:")
        for teacher in view_all_teachers():
            print(f"{teacher['id']} - {teacher['full_name']} - {teacher['department']}")
    
    def summary(self):
        students = view_all_students()
        teachers = view_all_teachers()
        count_students = len(students)
        count_teachers = len(teachers)
        average_score = sum(student["score"] for student in students) / count_students
        average_attendance = sum(student["presence"] for student in students) / count_students
        print("\nSchool Summary:")
        print(f"Students: {count_students}, Teachers: {count_teachers}")
        print(f"Average Score: {average_score:.1f}")
        print(f"Average Attendance: {average_attendance:.1f}%")
    
    def register_student(self, *ignored):
        self.deny("register students")
    def set_pay(self, *ignored):
        self.deny("change staff pay")