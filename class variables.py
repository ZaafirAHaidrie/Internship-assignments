class Student:

    class_year = 2024        #class variable
    num_students = 0

    def __init__(self,name,age):
        self.name = name
        self.age = age
        Student.num_students +=1

Student1 = Student("Spongebob", 30)
Student2 = Student("Patrick", 35)
Student3 = Student("Squidward", 55)
Student4 = Student("Sandy",27)

print(f"My graduating class of {Student.class_year} has {Student.num_students} students")
print(Student1.name)
print(Student2.name)
print(Student3.name)
print(Student4.name)