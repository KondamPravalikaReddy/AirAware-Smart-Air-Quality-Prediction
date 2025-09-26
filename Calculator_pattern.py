# Structural Pattern Matching Calculator

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
op = input("Enter operator (+, -, *, /, %, //, **): ")

match op:
    case '+':
        print("Result:", a + b)
    case '-':
        print("Result:", a - b)
    case '*':
        print("Result:", a * b)
    case '/':
        if b != 0:
            print("Result:", a / b)
        else:
            print("Error: Division by zero!")
    case '%':
        print("Result:", a % b)
    case '//':
        print("Result:", a // b)
    case '':
        print("Result:", a ** b)
    case _:
        print("Invalid Operator")
