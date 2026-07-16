student_records = [
    {"id": 1, "full_name": "Sakeena Batool", "grade": "11-A", "score": 95, "presence": 98},
    {"id": 2, "full_name": "Abdul Samad", "grade": "11-B", "score": 88, "presence": 92},
    {"id": 3, "full_name": "Faaiz Khan", "grade": "11-C", "score": 76, "presence": 85},
    {"id": 4, "full_name": "Ahmed Raza", "grade": "11-A", "score": 92, "presence": 97},
    {"id": 5, "full_name": "Juwairiah Awais", "grade": "11-B", "score": 84, "presence": 90},
]

teacher_records = [
    {"id": 101, "full_name": "Mr. Ahmed Maqsood", "department": "Mathematics", "pay": 50000},
    {"id": 102, "full_name": "Mr. Rao Habib", "department": "English", "pay": 48000},
    {"id": 103, "full_name": "Mr. Usama Virk ", "department": "Computer Science", "pay": 52000},
    {"id": 104, "full_name": "Mr. Bari", "department": "History", "pay": 47000}
]

def find_student(sid):
    for student in student_records:
        if student["id"] == sid:
            return student
    return None

def find_teacher(tid):
    for teacher in teacher_records:
        if teacher["id"] == tid:
            return teacher
    return None

class SchoolMember:
    def __init__(self, full_name, id_number):
        self.full_name = full_name
        self.id_number = id_number
        self.position = "Member"
    
    def display(self):
        print(f"{self.position}: {self.full_name} (ID {self.id_number})")
    
    def list_students(self):
        print("\nStudents:")
        for student in student_records:
            print(f"{student['id']} - {student['full_name']} - {student['grade']}")
    
    def deny(self, action):
        print(f"{self.position} is not permitted to {action}")

class Teacher(SchoolMember):
    def __init__(self, full_name, id_number, department):
        super().__init__(full_name, id_number)
        self.position = "Teacher"
        self.department = department
    
    def list_students(self):
        print(f"\nStudents ({self.department} class):")
        for student in student_records:
            print(f"{student['id']} - {student['full_name']} - {student['grade']} - "
                  f"Score {student['score']} - Presence {student['presence']}%")
    
    def update_marks(self, sid, score):
        student = find_student(sid)
        if student:
            student["score"] = score
            print(f"Updated score for {student['full_name']} to {score}")
        else:
            print(f"No student found with ID {sid}")
    
    def update_attendance(self, sid, presence):
        student = find_student(sid)
        if student:
            student["presence"] = presence
            print(f"Updated attendance for {student['full_name']} to {presence}%")
        else:
            print(f"No student found with ID {sid}")
    
    def list_teachers(self):
        self.deny("list teachers")
    def register_student(self, *ignored):
        self.deny("register students")
    def remove_student(self, *ignored):
        self.deny("remove students")

class Principal(SchoolMember):
    def __init__(self, full_name, id_number):
        super().__init__(full_name, id_number)
        self.position = "Principal"

    def list_students(self):
        print("\nStudents (Principal view):")
        for student in student_records:
            print(f"{student['id']} - {student['full_name']} - {student['grade']} - "
                  f"Score {student['score']} - Presence {student['presence']}%")
    
    def list_teachers(self):
        print("\nTeachers:")
        for teacher in teacher_records:
            print(f"{teacher['id']} - {teacher['full_name']} - {teacher['department']}")
    
    def summary(self):
        count_students = len(student_records)
        count_teachers = len(teacher_records)
        average_score = sum(student["score"] for student in student_records) / count_students
        average_attendance = sum(student["presence"] for student in student_records) / count_students
        print("\nSchool Summary:")
        print(f"Students: {count_students}, Teachers: {count_teachers}")
        print(f"Average Score: {average_score:.1f}")
        print(f"Average Attendance: {average_attendance:.1f}%")
    
    def register_student(self, *ignored):
        self.deny("register students")
    def set_pay(self, *ignored):
        self.deny("change staff pay")

class Admin(SchoolMember):
    def __init__(self, full_name, id_number):
        super().__init__(full_name, id_number)
        self.position = "Admin"
    
    def list_students(self):
        print("\nStudents (Admin view):")
        for student in student_records:
            print(student)

    def list_teachers(self):
        print("\nStaff (Admin view):")
        for teacher in teacher_records:
            print(teacher)
    
    def register_student(self, sid, full_name, grade, score=0, presence=0):
        student_records.append({"id": sid, "full_name": full_name, "grade": grade,
                                 "score": score, "presence": presence})
        print(f"Registered student {full_name} with ID {sid}")
    
    def modify_student(self, sid, field, value):
        student = find_student(sid)
        if student and field in student:
            student[field] = value
            print(f"Updated {field} for {student['full_name']} to {value}")
        else:
            print(f"Update failed")
    
    def remove_student(self, sid):
        student = find_student(sid)
        if student:
            student_records.remove(student)
            print(f"Removed student {student['full_name']} with ID {sid}")
        else:
            print(f"Removal Failed")
    
    def register_teacher(self, tid, full_name, department, pay):
        teacher_records.append({"id": tid, "full_name": full_name, "department": department, "pay": pay})
        print(f"Registered teacher {full_name} with ID {tid}")
    
    def set_pay(self, tid, pay):
        teacher = find_teacher(tid)
        if teacher:
            teacher["pay"] = pay
            print(f"Updated pay for {teacher['full_name']} to {pay}")
        else:
            print("Update failed")
    
    def remove_teacher(self, tid):
        teacher = find_teacher(tid)
        if teacher:
            teacher_records.remove(teacher)
            print(f"Removed teacher {teacher['full_name']} with ID {tid}")
        else:
            print("Removal failed")


def login():
    print("Who is viewing?")
    print("1. Teacher")
    print("2. Principal")
    print("3. Admin")
    choice = input("Enter choice (1-3): ")

    if choice == "1":
        return Teacher("Mr. Ahmed Maqsood", 101, "Mathematics")
    elif choice == "2":
        return Principal("Mr. Shahzad", 201)
    elif choice == "3":
        return Admin("Head Admin", 901)
    else:
        print("Invalid choice")
        return None


def teacher_menu(user):
    while True:
        print("\n1. View Students\n2. Update Marks\n3. Update Attendance\n4. View Teachers\n5. Register Student\n6. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            user.list_students()
        elif choice == "2":
            sid = int(input("Student ID: "))
            score = int(input("New score: "))
            user.update_marks(sid, score)
        elif choice == "3":
            sid = int(input("Student ID: "))
            presence = int(input("New attendance: "))
            user.update_attendance(sid, presence)
        elif choice == "4":
            user.list_teachers()
        elif choice == "5":
            user.register_student()
        elif choice == "6":
            break
        else:
            print("Invalid choice")


def principal_menu(user):
    while True:
        print("\n1. View Students\n2. View Teachers\n3. School Summary\n4. Register Student\n5. Set Pay\n6. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            user.list_students()
        elif choice == "2":
            user.list_teachers()
        elif choice == "3":
            user.summary()
        elif choice == "4":
            user.register_student()
        elif choice == "5":
            user.set_pay()
        elif choice == "6":
            break
        else:
            print("Invalid choice")


def admin_menu(user):
    while True:
        print("\n1. View Students\n2. View Teachers\n3. Register Student\n4. Modify Student\n5. Remove Student"
              "\n6. Register Teacher\n7. Set Pay\n8. Remove Teacher\n9. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            user.list_students()
        elif choice == "2":
            user.list_teachers()
        elif choice == "3":
            sid = int(input("New student ID: "))
            full_name = input("Full name: ")
            grade = input("Grade: ")
            score = int(input("Score: "))
            presence = int(input("Presence: "))
            user.register_student(sid, full_name, grade, score, presence)
        elif choice == "4":
            sid = int(input("Student ID: "))
            field = input("Field to update: ")
            value = input("New value: ")
            user.modify_student(sid, field, value)
        elif choice == "5":
            sid = int(input("Student ID: "))
            user.remove_student(sid)
        elif choice == "6":
            tid = int(input("New teacher ID: "))
            full_name = input("Full name: ")
            department = input("Department: ")
            pay = int(input("Pay: "))
            user.register_teacher(tid, full_name, department, pay)
        elif choice == "7":
            tid = int(input("Teacher ID: "))
            pay = int(input("New pay: "))
            user.set_pay(tid, pay)
        elif choice == "8":
            tid = int(input("Teacher ID: "))
            user.remove_teacher(tid)
        elif choice == "9":
            break
        else:
            print("Invalid choice")


if __name__ == '__main__':
    user = login()
    if user:
        user.display()
        if isinstance(user, Teacher):
            teacher_menu(user)
        elif isinstance(user, Principal):
            principal_menu(user)
        elif isinstance(user, Admin):
            admin_menu(user)