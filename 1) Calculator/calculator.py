import random


print("Welcome to World's best calculator\n")
while True:
    try:
        ask = input("Addition = A, Subtraction = S, Multiplication = M, Division = D: ")
        if ask.upper() == "ADDITION" or ask.upper() == "A":
            sum1 = float(input ("Enter the first number: "))
            sum2 = float(input ("Enter the second number: "))
            total = sum1 + sum2
            print ("The total is " + str (total))
        elif ask.upper() == "SUBTRACTION" or ask.upper() == "S":
            sum1 = float(input ("Enter the first number: "))
            sum2 = float(input ("Enter the second number: "))
            total = sum1 - sum2
            print("The difference is " + str(total))
        elif ask.upper() == "DIVISION" or ask.upper() == "D":
            sum1 = float(input ("Enter the first number: "))
            sum2 = float(input ("Enter the second number: "))
            try:
                total1 = sum1 // sum2
                total2 = sum1 / sum2
                remainder = sum1 % sum2
                print("Quotient is",str(total1),"and Remainder is",str(remainder),"\nAnswer is",total2)
            except:
                if sum2 == 0:
                    print("Answer is infinity")
                else:
                    pass
        elif ask.upper() == "MULTIPLICATION" or ask.upper() == "M":
            sum1 = float(input ("Enter the first number: "))
            sum2 = float(input ("Enter the second number: "))
            total = sum1 * sum2
            print("The product is " + str(total))
        else:
            pass
    except:
        print("Sorry that incorrect please try again")
