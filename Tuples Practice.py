#Question 1: How do you create an empty tuple?
emt = tuple()
print(emt)

#Question 2: Create a tuple containing the numbers 10, 20, and 30. Write the code to print out just the second item (20).
emt = (10,20,30)
print(emt[1])

#Question 3 (The Trap!): Try creating a tuple that contains just one single item: the number 5. Check its type using type().
onevalt = (5,)
print(type(onevalt))

#Question 4: how could you "add" a new item "orange" to the end of that colors tuple to create a brand new tuple?
color = ("red","yellow,","yellow")
new_colors = color + ("orange",)
print(new_colors)

#Question 5: Imagine you have a tuple coordinates = (40.7128, -74.0060). 
#Write a single line of code to "unpack" this tuple into two separate variables named latitude and longitude.
coordinates = (40.7128,-74.0060)
(longitude,latitude) = coordinates
print(longitude)
print(latitude)

#Question 6: Given the tuple numbers = (1, 2, 3, 2, 4, 2, 5), 
# write a line of code to find out how many times the number 2 appears.
numbers = (1,2,3,2,4,2,5)
print(numbers.count(2))


#Question 7: What happens if a tuple contains a list inside it? For example:
#my_tuple = (1, 2, ["apple", "banana"])
#Can you change "banana" to "cherry"? Try running code to do that. If tuples are immutable, why does this work (or not work)?
my_tuple = (1,2,['apple','banana'])
my_tuple[2][1] = 'cherry'
print(my_tuple)

#Question 8: The Data Cleaner (Tuple to List and Back)
#Imagine you download a user profile from a secure database as a tuple because the database wants to ensure the data 
#user_profile = ("Alex", "alex@email.com", "Active", "User")
#Write code that converts this tuple into a list, changes the status from "Active" to "Suspended", 
#and converts it back into a final tuple called updated_profile.

lst = []
user_profile = ("Alex", "alex@email.com", "Active", "User")
for i in user_profile:
    lst.append(i)
lst[2] = "Suspended"
updated_user_profile = tuple(lst)
print(updated_user_profile)