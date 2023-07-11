from cryptography.fernet import Fernet
import getpass

print("Welcome to Password Manager")
print("Caution: If you stop the script it the middle of an action the (Title | Username | Password) might be deleted\n")


def write_key():
    key2 = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key2)


def load_key():
    file = open("key.key","rb")
    key2 = file.read()
    file.close()
    return key2


write_key()
key = load_key()
fernet = Fernet(key)


def create_master_key():
    x = input("Create your Master Key: ")
    with open("master.txt","w") as file:
        file.write(fernet.encrypt(x.encode()).decode())
        print("Master key has been created")


create_master_key()
MasterKey = fernet.encrypt(getpass.getpass("Enter the Master Password: ").encode()).decode()


def see():
    with open("password will save.txt","r+") as file:
        for line in file.readlines():
            storing_data = line.strip()
            title,user,password = storing_data.split("|")
            print("Title:",fernet.decrypt(title.encode()).decode(),"| Username:",fernet.decrypt(
                user.encode()).decode(),"| Password:",fernet.decrypt(password.encode()).decode())


def add():
    title = input("Enter the title: ")
    user = input("Enter the Username: ")
    password = input("Enter the Password: ")
    with open("password will save.txt","a") as file:
        file.write(fernet.encrypt(title.encode()).decode() + "|" + fernet.encrypt(
            user.encode()).decode() + "|" + fernet.encrypt(password.encode()).decode() + "\n")


def delete():
    with open("password will save.txt","r") as file:
        for line in file.readlines():
            storing_data = line.strip()
            title,user,password = storing_data.split("|")
            deleting = "Title:",fernet.decrypt(title.encode()).decode(),"| Username:",fernet.decrypt(
                user.encode()).decode(),"| Password:",fernet.decrypt(password.encode()).decode()
            while True:
                print("Title:",fernet.decrypt(title.encode()).decode(),"| Username:",fernet.decrypt(
                    user.encode()).decode(),"| Password:",fernet.decrypt(password.encode()).decode())
                ask2 = input("Do yo want to delete this [yes,no]: ")
                if ask2[0].upper() == "Y":
                    with open("password will save.txt","r") as file2:
                        data = file2.readlines()
                    with open("password will save.txt","w") as file3:
                        for x in data:
                            storing_data2 = x.strip()
                            title2,user2,password2 = storing_data2.split("|")
                            deleting2 = "Title:",fernet.decrypt(title2.encode()).decode(),"| Username:",fernet.decrypt(
                                user2.encode()).decode(),"| Password:",fernet.decrypt(password2.encode()).decode()
                            if deleting2 != deleting:
                                file3.write(x)
                    break
                elif ask2[0].upper() == "N":
                    break
                else:
                    print("You have not typed [Yes,No]")


with open("master.txt","r") as lines:
    for z in lines.readlines():
        if fernet.decrypt(MasterKey.encode()).decode() in fernet.decrypt(z.strip().encode()).decode():
            while True:
                ask = input(
                    "Would you like to add a new title/username/password or view existing ones or delete the existing ones (view,add,delete), type quit to quit: ").lower()
                if ask == "":
                    print("sorry, you did not typed (view,add,delete,quit)")
                elif ask[0].lower() == "q":
                    exit()
                elif ask[0].lower() == "v":
                    see()
                elif ask[0].lower() == "a":
                    add()
                elif ask[0].lower() == "d":
                    delete()
                    continue
                else:
                    print("sorry, you did not typed (view,add,delete,quit)")
                    continue
        else:
            print("Incorrect password, session closed")
            exit()
