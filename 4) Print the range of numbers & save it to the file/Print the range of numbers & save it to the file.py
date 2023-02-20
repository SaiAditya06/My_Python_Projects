with open(r"file.txt","w+") as file2:
    file2.close()

while True:
    try:
        ask = int(input("Enter the number to print the range & save it to the file: "))
    except:
        print("Sorry that's not a number")
    else:
        break

for x in range(1,ask + 1):
    y = x
    num = ask + 1
    while True:
        if len(str(y)) != len(str(num)):
            y = "0" + str(y)
        if len(str(y)) == len(str(num)):
            with open(r"file.txt","a") as file:
                file.write(str(y) + "\n")
                print(y)
            break
