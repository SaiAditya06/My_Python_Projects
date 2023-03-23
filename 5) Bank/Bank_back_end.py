from cryptography.fernet import Fernet
import time


def write_key():
    key2 = Fernet.generate_key()
    with open("key2.key","wb") as key_file:
        key_file.write(key2)


def load_key():
    f = open("key2.key","rb")
    key2 = f.read()
    f.close()
    return key2


#after you run it for the first please comment 29
#write_key()


key = load_key()
fernet = Fernet(key)


def login1(user_name,pass_word):
    user___name = None
    pass___word = None
    mor = None
    with open("login passwords money.txt","r") as key_file:
        for x in key_file.readlines():
            storing_data = x.strip()
            user__name,pass__word,mon = storing_data.split("|")
            user___name = fernet.decrypt(user__name.encode()).decode()
            pass___word = fernet.decrypt(pass__word.encode()).decode()
            mor = fernet.decrypt(mon.encode()).decode()
            if user_name == user___name and pass_word == pass___word:
                count = 0
                while count <= 3:
                    count += 1
                    print(100 * "\n")
                    print("Enter your username:",user_name)
                    print("Enter your password: ")
                    print("")
                    print("logging in.")
                    time.sleep(1)
                while count <= 6:
                    count += 1
                    print(100 * "\n")
                    print("Enter your username:",user_name)
                    print("Enter your password: ")
                    print("")
                    print("logging in..")
                    time.sleep(1)
                while count < 9:
                    count += 1
                    print(100 * "\n")
                    print("Enter your username:",user_name)
                    print("Enter your password: ")
                    print("")
                    print("logging in...")
                    time.sleep(1)
                print("Login successful")
                return {"tof": True,"user": user_name,"pass": pass_word,"money": mor}
        if user_name != user___name and pass_word != pass___word:
            if True:
                count = 0
                while count <= 3:
                    count += 1
                    print(100 * "\n")
                    print("Enter your username:",user_name)
                    print("Enter your password: ")
                    print("")
                    print("logging in.")
                    time.sleep(1)
                while count <= 6:
                    count += 1
                    print(100 * "\n")
                    print("Enter your username:",user_name)
                    print("Enter your password: ")
                    print("")
                    print("logging in..")
                    time.sleep(1)
                while count < 9:
                    count += 1
                    print(100 * "\n")
                    print("Enter your username:",user_name)
                    print("Enter your password: ")
                    print("")
                    print("logging in...")
                    time.sleep(1)
                print("Login unsuccessful")
                return {"tof": False,"user": user_name,"pass": pass_word,"money": mor}


def login(xx,yy):
    x = login1(xx,yy)
    tof = x.get("tof")
    username2 = x.get("user")
    password2 = x.get("pass")
    money_money = float(x.get("money"))
    while True:
        if tof:
            ask2 = input(
                "Do you want to your money to be deposited(d) / withdraw(w) / transfer(t) / view balance(v) / logout(l) / remove account(r): ")
            if ask2 == "":
                print(
                    "Sorry you did not say money to be deposited(d) / withdraw(w) / transfer(t) / view balance(v) / logout(l) / remove account(r)")
            elif ask2[0].upper() == "D":
                while True:
                    try:
                        add = float(input("How much money do you want to deposit: "))
                    except:
                        print("Sorry that's not a number")
                    else:
                        break
                with open("login passwords money.txt","r") as key_file:
                    data = key_file.readlines()
                    if True:
                        if True:
                            with open("login passwords money.txt","w") as file3:
                                for yyy in data:
                                    storing_data2 = yyy.strip()
                                    user____name,pass____word,money3 = storing_data2.split("|")
                                    money4 = money_money + add
                                    deleting2 = "User:",fernet.decrypt(
                                        user____name.encode()).decode(),"| Password:",fernet.decrypt(
                                        pass____word.encode()).decode(),"| Money:",str(
                                        float(fernet.decrypt(money3.encode()).decode()))
                                    deleting = "User:",username2,"| Password:",password2,"| Money:",str(money_money)
                                    if deleting2 != deleting:
                                        file3.write(yyy)
                                    elif deleting2 == deleting:
                                        money_money += add
                                        file3.write(
                                            fernet.encrypt(username2.encode()).decode() + "|" + fernet.encrypt(
                                                password2.encode()).decode() + "|" + fernet.encrypt(
                                                str(money4).encode()).decode() + "\n")
            elif ask2[0].upper() == "W":
                while True:
                    try:
                        withdraw = float(input("How much money do you want to withdraw: "))
                    except:
                        print("Sorry that's not a number")
                    else:
                        break
                with open("login passwords money.txt","r") as key_file:
                    data = key_file.readlines()
                    if True:
                        if True:
                            with open("login passwords money.txt","w") as file3:
                                if True:
                                    if True:
                                        if money_money >= withdraw:
                                            for yyy in data:
                                                storing_data2 = yyy.strip()
                                                user____name,pass____word,money3 = storing_data2.split("|")
                                                money4 = money_money - withdraw
                                                deleting2 = "User:",fernet.decrypt(
                                                    user____name.encode()).decode(),"| Password:",fernet.decrypt(
                                                    pass____word.encode()).decode(),"| Money:",str(
                                                    float(fernet.decrypt(money3.encode()).decode()))
                                                deleting = "User:",username2,"| Password:",password2,"| Money:",str(
                                                    money_money)
                                                if deleting2 != deleting:
                                                    file3.write(yyy)
                                                elif deleting2 == deleting:
                                                    money_money -= withdraw
                                                    file3.write(
                                                        fernet.encrypt(
                                                            username2.encode()).decode() + "|" + fernet.encrypt(
                                                            password2.encode()).decode() + "|" + fernet.encrypt(
                                                            str(money4).encode()).decode() + "\n")
                                        else:
                                            print("Sorry you dont have enough money")
                                            withdraw = 0

                                            for yyy in data:
                                                storing_data2 = yyy.strip()
                                                user____name,pass____word,money3 = storing_data2.split("|")
                                                money4 = money_money - withdraw
                                                deleting2 = "User:",fernet.decrypt(
                                                    user____name.encode()).decode(),"| Password:",fernet.decrypt(
                                                    pass____word.encode()).decode(),"| Money:",str(
                                                    float(fernet.decrypt(money3.encode()).decode()))
                                                deleting = "User:",username2,"| Password:",password2,"| Money:",str(
                                                    money_money)
                                                if deleting2 != deleting:
                                                    file3.write(yyy)
                                                elif deleting2 == deleting:
                                                    money_money -= withdraw
                                                    file3.write(
                                                        fernet.encrypt(
                                                            username2.encode()).decode() + "|" + fernet.encrypt(
                                                            password2.encode()).decode() + "|" + fernet.encrypt(
                                                            str(money4).encode()).decode() + "\n")
            elif ask2[0].upper() == "V":
                with open("login passwords money.txt","r") as file:
                    for line in file.readlines():
                        storing_data = line.strip()
                        user,passing,money = storing_data.split("|")
                        if fernet.decrypt(user.encode()).decode() == username2 and fernet.decrypt(
                                passing.encode()).decode() == password2:
                            print("Money:",float(fernet.decrypt(money.encode()).decode()))
            elif ask2[0].upper() == "L":
                return
            elif ask2[0].upper() == "R":
                ask4 = input("Are you sure you want to delete account | yes (y) / no (n)")
                if ask4[0].upper() == "Y":
                    if money_money <= 0:
                        if True:
                            if True:
                                deleting = "User:",username2,"| Password:",password2,"| Money:",str(money_money)
                                if True:
                                    if True:
                                        with open("login passwords money.txt",
                                                  "r") as file2:
                                            data = file2.readlines()
                                        with open("login passwords money.txt",
                                                  "w") as file3:
                                            for x in data:
                                                storing_data2 = x.strip()
                                                user22,password22,money22 = storing_data2.split("|")
                                                deleting2 = "User:",fernet.decrypt(
                                                    user22.encode()).decode(),"| Password:",fernet.decrypt(
                                                    password22.encode()).decode(),"| Money:",str(
                                                    float(fernet.decrypt(money22.encode()).decode()))
                                                if deleting2 != deleting:
                                                    file3.write(x)
                    else:
                        print("First withdraw your money then you can remove your account")
                    return

            elif ask2[0].upper() == "T":
                with open("login passwords money.txt","r") as file:
                    file2 = file.readlines()
                    for z in file2:
                        m = z.strip()
                        o = m.split("|")[0]
                        n = fernet.decrypt(o.encode()).decode()
                        file3ing = []
                        if username2 != n:
                            file3ing.append(z)
                    for x,y in enumerate(file3ing,1):
                        storing_data = y.strip()
                        user = storing_data.split("|")[0]
                        user_name = fernet.decrypt(user.encode()).decode()
                        print(str(x) + ") " + user_name)
                    else:
                        while True:
                            try:
                                if len(file3ing) >= 1:
                                    ask3 = int(input(
                                        "Who do you want to transfer money to (enter the number left side of the the person you want to transfer money to): "))
                                else:
                                    print("Sorry you are the only customer")
                            except:
                                print("Sorry that's not a number")
                            else:
                                break

                        #

                        for xx,yy in enumerate(file3ing,1):
                            number = xx
                            storing_data = yy.strip()
                            user,passing,mon_mon = storing_data.split("|")
                            user_name = fernet.decrypt(user.encode()).decode()
                            pas_word = fernet.decrypt(passing.encode()).decode()
                            mon_mon_ = float(fernet.decrypt(mon_mon.encode()).decode())
                            if ask3 == xx:
                                while True:
                                    try:
                                        send = float(input(
                                            "How much money do you want send: "))
                                    except:
                                        print("Sorry that's not a number")
                                    else:
                                        break
                                with open("login passwords money.txt",
                                          "r") as key_file:
                                    data = key_file.readlines()
                                    if True:
                                        if True:
                                            with open("login passwords money.txt",
                                                      "w") as file3:
                                                if True:
                                                    if money_money >= send:
                                                        for yyy in data:
                                                            storing_data2 = yyy.strip()
                                                            user____name,pass____word,money3 = storing_data2.split("|")
                                                            money4 = float(mon_mon_) + send
                                                            money5 = money_money - send
                                                            deleting3 = "User:",fernet.decrypt(
                                                                user____name.encode()).decode(),"| Password:",fernet.decrypt(
                                                                pass____word.encode()).decode(),"| Money:",str(
                                                                float(fernet.decrypt(money3.encode()).decode()))
                                                            deleting = "User:",username2,"| Password:",password2,"| Money:",str(
                                                                float(money_money))
                                                            deleting2 = "User:",user_name,"| Password:",pas_word,"| Money:",str(
                                                                float(mon_mon_))
                                                            if deleting3 != deleting and deleting3 != deleting2:
                                                                file3.write(yyy)
                                                            elif deleting3 == deleting:
                                                                money_money -= send
                                                                file3.write(
                                                                    fernet.encrypt(
                                                                        username2.encode()).decode() + "|" + fernet.encrypt(
                                                                        password2.encode()).decode() + "|" + fernet.encrypt(
                                                                        str(money5).encode()).decode() + "\n")
                                                            elif deleting3 == deleting2:
                                                                mon_mon_ += send
                                                                file3.write(
                                                                    fernet.encrypt(
                                                                        user_name.encode()).decode() + "|" + fernet.encrypt(
                                                                        pas_word.encode()).decode() + "|" + fernet.encrypt(
                                                                        str(money4).encode()).decode() + "\n")
                                                    else:
                                                        print("Sorry you dont have enough money")
                                                        send = 0
                                                        for yyy in data:
                                                            storing_data2 = yyy.strip()
                                                            user____name,pass____word,money3 = storing_data2.split("|")
                                                            money4 = float(mon_mon_) + send
                                                            money5 = money_money - send
                                                            deleting3 = "User:",fernet.decrypt(
                                                                user____name.encode()).decode(),"| Password:",fernet.decrypt(
                                                                pass____word.encode()).decode(),"| Money:",str(
                                                                float(fernet.decrypt(money3.encode()).decode()))
                                                            deleting = "User:",username2,"| Password:",password2,"| Money:",str(
                                                                float(money_money))
                                                            deleting2 = "User:",user_name,"| Password:",pas_word,"| Money:",str(
                                                                float(mon_mon_))
                                                            if deleting3 != deleting and deleting3 != deleting2:
                                                                file3.write(yyy)
                                                            elif deleting3 == deleting:
                                                                money_money -= send
                                                                file3.write(
                                                                    fernet.encrypt(
                                                                        username2.encode()).decode() + "|" + fernet.encrypt(
                                                                        password2.encode()).decode() + "|" + fernet.encrypt(
                                                                        str(money5).encode()).decode() + "\n")
                                                            elif deleting3 == deleting2:
                                                                mon_mon_ += send
                                                                file3.write(
                                                                    fernet.encrypt(
                                                                        user_name.encode()).decode() + "|" + fernet.encrypt(
                                                                        pas_word.encode()).decode() + "|" + fernet.encrypt(
                                                                        str(money4).encode()).decode() + "\n")
                        if ask3 != number:
                            print("Sorry there is no person who you chosen")
            else:
                print(
                    "Sorry you did not say money to be deposited(d) / withdraw(w) / transfer(t) / view balance(v) / logout(l) / remove account(r)")
        if not tof:
            return


def account_create():
    while True:
        u = input("Enter the Username: ")
        with open("login passwords money.txt","r") as file2:
            data = file2.readlines()
            if not data:
                break
            for x in data:
                data0 = x.strip()
                data1 = data0.split("|")[0]
                data2 = fernet.decrypt(data1.encode()).decode()
                if data2 == u:
                    print("Sorry the username is taken")
                    usman = True
                    break
                else:
                    usman = False
            if usman:
                continue
            if not usman:
                break

    p = input("Enter the Password: ")
    m = "0.0"
    with open("login passwords money.txt","a") as file:
        file.write(fernet.encrypt(u.encode()).decode() + "|" + fernet.encrypt(
            p.encode()).decode() + "|" + fernet.encrypt(m.encode()).decode() + "\n")
