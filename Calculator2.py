
numbers = []
operations = []

while True:
    print("Enter 'q' to exit")
    digit = input("Enter your digit: ")
    
    if digit == 'q':
        break
        
    if '.' in digit:
        num = float(digit)
    else:
        num = int(digit)
        
    numbers.append(num)
    print("Your numbers are:", numbers)

if len(numbers) > 1:
    operator = input("\nEnter operator [+,-,*,/]: ")
    result = numbers[0]
    for num in numbers[1:]:
        if operator == "+":
          
            old_result = result
            result = result + num 
            print(old_result, "+", num, "=", result)

        elif operator == "-":   
            old_result = result
            result = result - num
            print(old_result, "-", num, "=", result)

        elif operator == "*":
            old_result = result
            result = result * num
            print(old_result, "*", num, "=", result)

        elif operator == "/":
            if num != 0:
                old_result = result
                result = result / num
                print(old_result, "/", num, "=", result)
            else: 
                print("Cannot divide by 0")   
        else: 
            print("Incorrect operator entered")
            break 
            
    print("\nFinal Result:", result)

else:
    print("Invalid input, enter atleast 2 numbers")
