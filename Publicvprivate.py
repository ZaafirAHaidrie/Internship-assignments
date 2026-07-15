class Cat:
    def __init__(self, name, eye_color):
        self.name = name
        self.breed = "Persian"       
        self.is_alive = True          
        self.__eye_color = eye_color  

    def eat(self):
        print(f"{self.name} is eating")

    def sleep(self):
        print(f"{self.name} is sleeping")

    def speak(self):
        print("MEOW!")

    def get_eye_color(self):          
        return self.__eye_color


class Kitten(Cat):
    def __init__(self, name, eye_color):
        super().__init__(name, eye_color)

mother = Cat("Smokey", eye_color="blue")

kitten1 = Kitten("Leo", eye_color="green")
kitten2 = Kitten("Milo", eye_color="amber")

print("\n")
print(mother.name, mother.breed, mother.is_alive, mother.get_eye_color())
print(kitten1.name, kitten1.breed, kitten1.is_alive, kitten1.get_eye_color())
print(kitten2.name, kitten2.breed, kitten2.is_alive, kitten2.get_eye_color())
print("\n")