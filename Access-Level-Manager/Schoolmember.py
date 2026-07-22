from Helpers import view_all_students
class SchoolMember:
    def __init__(self,full_name,id_number):
        self.full_name = full_name
        self.id_number = id_number
        self.position = "Member"
    
    def display(self):
        print(f"{self.position}: {self.full_name} (ID {self.id_number})")
    
    def studentlist(self):
        print("\nList of Students:")
        for student in view_all_students():
            print(f"{student['id']} - {student['full_name']} - {student['grade']}")
    def deny(self,action):
        print(f"{self.position} is not permitted to {action}")