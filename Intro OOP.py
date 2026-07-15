from car import Car

car1 = Car("Elantra", 2024, "red", False)
car2 = Car("Civic", 2025, "blue", True)
car3 = Car("Fortuner", 2026, "white", True)


print(car3.model)
print(car3.year)
print(car3.color)
print(car3.for_sale)

car1.describe()