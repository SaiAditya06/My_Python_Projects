import getpass
import Bank_back_end

print("Welcome to the Commercial Bank of India")

while True:
    ask = input("Do you want to Login (l) or Register (r) for a bank account: ")
    if ask == "":
        print("Sorry you did not type Login or Register")
    elif ask[0].upper() == "L":
        username = input("Enter your Username: ")
        password = getpass.getpass("Enter your Password: ")
        Bank_back_end.login(username,password)
    elif ask[0].upper() == "R":
        Bank_back_end.account_create()
    else:
        print("Sorry you did not type Login or Register")
