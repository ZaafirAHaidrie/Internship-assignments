
choice = input("do you want to do integer calculations or float calculations?")

if choice == 'integer':
    int1 = int(input("Enter the first integer: "))

    int2 = int(input("Enter the second integer: "))

    print("You entered:", int1, "and", int2)
    print("enter operation to be done:")

    operation = input("+,-,*,/:  ")
    if operation == "+":
        answer = int1 + int2 
        print(int1,"+",int2,"=",answer)

    elif operation == "-":   
        answer = int1 - int2
        print(int1,"-",int2,"=",answer)

    elif operation == "*":
        answer = int1 * int2
        print(int1,"*",int2,"=",answer)

    elif operation == "/":
        
        if int2 != 0:
            answer = int1/int2
            print(int1,"/",int2,"=",answer)
        else: print("Cannot divide by 0")   
    else: print("incorrect operation entered")

elif choice == 'float':
    float1 = float(input("Enter the first decimal: "))

    float2 = float(input("Enter the second decimal: "))

    print("You entered:", float1, "and", float2)
    print("enter operation to be done:")

    operation = input("+,-,*,/:  ")
    if operation == "+":
        answer = float1 + float2 
        print(float1,"+",float2,"=",answer)

    elif operation == "-":
        answer = float1 - float2
        print(float1,"-",float2,"=",answer)

    elif operation == "*":
        answer = float1 * float2
        print(float1,"*",float2,"=",answer)

    elif operation == "/":
        
        if float2 != 0:
            answer = float1/float2
            print(float1,"/",float2,"=",answer)
        else: print("Cannot divide by 0")   
    else: print("incorrect operation entered")
else:
    print("ERROR! [INVALID INPUT]")
