while True:
    
    expression = input("\nEnter expression or 'quit' if done: ")

    if expression == 'quit':
        print("Program exited by user")
        break
    parts = expression.split()

    if len(parts) < 3 or len(parts) % 2 == 0:
        print("\nInvalid expression!")
        continue
    numbers = []
    operators = []
    valid = True

    for i in range(len(parts)):
        if i % 2 == 0:  
            if '.' in parts[i]:
                numbers.append(float(parts[i]))
            else:
                numbers.append(int(parts[i]))
        else:           
            if parts[i] in ['+', '-', '*', '/']:
                operators.append(parts[i])
            else:
                print("Invalid operator:", parts[i])
                valid = False
                break

    if not valid:
        continue
    result = numbers[0]

    for i in range(len(operators)):
        operation = operators[i]
        next_num = numbers[i + 1]

        if operation == '+':
            result = result + next_num
        elif operation == '-':
            result = result - next_num
        elif operation == '*':
            result = result * next_num
        elif operation == '/':
            if next_num == 0:
                print("Cannot divide by 0!")
                valid = False
                break
            result = result / next_num

    if valid:
        print("Answer:", result)