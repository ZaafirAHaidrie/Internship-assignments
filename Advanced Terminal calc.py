import math

def add(a,b):
    return a + b

def subtract(a,b):
    return a - b

def multiply(a,b):
    return a * b

def divide(a,b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a/ b 

def squareroot(a):
    if a < 0:
        raise ValueError("Cannot divide by zero")
    return math.sqrt(a)

def square(a):
    return a * a

def factorial(a):
    if a < 0:
        raise ValueError("Cannot take factorial of negative number")
    if not float(a).is_integer():
        raise ValueError("Factorial requires a whole number")
    return math.factorial(int(a))

def negate(a):
    return -a

def pi_value():
    return math.pi

def format(result):
    if isinstance(result,float):
        if result.is_integer():
            return int(result)
        return round(result,4)
    return result

def numinput(prompt="Enter number: "):
    while True:
        userinp = input(prompt).strip()
        try:
            if '.' in userinp:
                return float(userinp)
            return int(userinp)
        except ValueError:
            print("Invalid number, Try Again")

standard_ops = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}
advanced_ops = {
    'sqrt': squareroot,
    'sq': square,
    'fact': factorial,
    'neg': negate,
}

def visualization():
    print("=" * 65)
    print("                         CALCULATOR")
    print("=" * 65)
    print("Standard operations: + - * / [ASKS FOR SECOND NUMBER]")
    print("Advanced operations: sqrt  sq  fact  neg [APPLIES TO CURRENT RESULT]")
    print("Other:    pi      ")
    print("          =    (stop and show final result)")
    print("          q    (quit)")
    print("=" * 65)

def main():
    visualization()

    result = numinput("Enter your first number: ")
    while True:
        print("current result: ", format(result))
        op = input(
            "Enter operator [+ - * /], function [sqrt sq fact neg pi], "
            "'=' to finish, or 'q' to quit: "
        ).strip().lower()

        if op == 'q':
            print("Program Exited!")
            return
        if op == '=':
            break      
        old_result = result
        try:
            if op in standard_ops:
                next_num = numinput("Enter next number: ")
                result = format(standard_ops[op](result,next_num))
                print(old_result , op , next_num ,"=", result)
            
            if op in advanced_ops:
                result = format(advanced_ops[op](result))
                print(op, old_result, "=", result)

            else:
                print("Invalid operator, please try again")
        except ValueError as err:
            print("Error: ", err)
            result = old_result
    print("\nFinal Result:", format(result))

main()