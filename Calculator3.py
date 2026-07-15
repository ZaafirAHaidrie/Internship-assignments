numbers = []
operations = []

print("Enter your numbers and operators. Enter '=' to calculate or 'q' to quit.")

while True:
    digit = input("\nEnter your digit: ")
    if digit.lower() == 'q':
        break
    if '.' in digit:
        num = float(digit)
    else:
        num = int(digit)
    numbers.append(num)
    
    operator = input("Enter operator [+, -, *, /] or '=' to calculate: ")
    
    if operator == '=' or operator == 'q':
        break
    elif operator in ['+', '-', '*', '/']:
        operations.append(operator)
    else:
        print("Invalid operator! Exiting calculation.")
        break

if len(numbers) > 1 and len(operations) == len(numbers) - 1:
    result = numbers[0]
    
    for i in range(len(operations)):
        op = operations[i]
        next_num = numbers[i + 1]
        old_result = result
        
        if op == "+":
            result = result + next_num
            print(old_result, "+", next_num, "=", result)
        elif op == "-":
            result = result - next_num
            print(old_result, "-", next_num, "=", result)
        elif op == "*":
            result = result * next_num
            print(old_result, "*", next_num, "=", result)
        elif op == "/":
            if next_num != 0:
                result = result / next_num
                print(old_result, "/", next_num, "=", result)
            else:
                print("Error: Cannot divide by 0")
                result = None
                break
                
    if result is not None:
        print("\nFinal Result:", result)
else:
    print("Invalid input. You need at least 2 numbers and a matching operator.")