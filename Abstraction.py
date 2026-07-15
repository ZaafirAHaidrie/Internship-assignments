from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def go(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class Car(Vehicle):
    def go(self):
        print("You drive the car")

    def stop(self):
        print("You stop the car")

car = Car()

class Motorcycle(Vehicle):
    def go(self):
        print("You ride the motorcycle")

    def stop(self):
        print("You stop the motorycle")

motorcycle = Motorcycle()

class Boat(Vehicle):
    def go(self):
        print("You sail the boat")

    def stop(self):
        print("You anchor the boat")

boat = Boat()

print('\n')
boat.go()
boat.stop()
car.go()
car.stop()
print('\n')