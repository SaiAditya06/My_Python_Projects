from cryptography.fernet import Fernet
import os
import time
import random
import string

class Bank:
    def __init__(self, username, password,key_file_path="key.txt",passwords_will_save="login passwords money.txt"):
        self.username = username
        self.password = password
        self.money = 0.0
        self.transfer_id = None
        self.key_file_path = key_file_path
        self.passwords_will_save = passwords_will_save
        self.encrypted_key = None
        self.decrypted_key = None

    def write_key(self):
        if not os.path.exists(self.key_file_path):
            key = Fernet.generate_key()
            with open(self.key_file_path, "wb") as key_file:
                key_file.write(key)

    def load_key(self):
        while True:
            if os.path.exists(self.key_file_path):
                with open(self.key_file_path, "rb") as key_file:
                    key = key_file.read()
                    if key:
                        return key
            else:
                self.write_key()

    def encrypted_key_function(self, encrypt_key):
        fernet = Fernet(self.load_key())
        self.encrypted_key = fernet.encrypt(encrypt_key.encode()).decode()
        return self.encrypted_key

    def decrypted_key_function(self, decrypt_key):
        fernet = Fernet(self.load_key())
        self.decrypted_key = fernet.decrypt(decrypt_key.encode()).decode()
        return self.decrypted_key

    def login(self):
        with open(self.passwords_will_save, "a") as file:
            file.write("")
            file.close()
        if os.path.exists(self.passwords_will_save):
            with open(self.passwords_will_save, "r") as key_file:
                lines = key_file.readlines()
                if not lines:
                    print("Login unsuccessful\n")
                    return {"tof": False}
                for x in lines:
                    user_encrypt, passw_encrypt, money_encrypt, transfer_id_encrypt = x.strip("\n").split("|")
                    user_decrypt = self.decrypted_key_function(user_encrypt)
                    passw_decrypt = self.decrypted_key_function(passw_encrypt)
                    money_decrypt = self.decrypted_key_function(money_encrypt)
                    transfer_id_decrypt = self.decrypted_key_function(transfer_id_encrypt)
                    if self.username == user_decrypt and self.password == passw_decrypt:
                        print("Login successful\n")
                        self.transfer_id = transfer_id_decrypt
                        self.money = money_decrypt
                        return {"tof": True}
                else:
                    print("Login unsuccessful\n")
                    return {"tof": False}

    def account_create(self):
        with open(self.passwords_will_save, "a") as file:
            file.write("")
            file.close()
        while True:
            username = input("Enter the Username: ")
            with open(self.passwords_will_save, "r") as file:
                data = file.readlines()
                for x in data:
                    user = self.decrypted_key_function(x.strip("\n").split("|")[0])
                    if user == username:
                        print("Sorry, the username is taken")
                        break
                else:
                    if username == "" or " " in username:
                        print("Sorry, the username should not be blank or have spaces")
                    else:
                        break

        while True:
            password = input("Enter the Password: ")
            if password == "":
                print("Sorry, the password should not be blank")
                continue
            else:
                break
        with open(self.passwords_will_save, "a") as file2:
            while True:
                random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
                for x in data:
                    if random_string == x.strip("\n").split("|")[3]:
                        break
                break
            file2.write(self.encrypted_key_function(username)+ "|"+ self.encrypted_key_function(password)+ "|"+ self.encrypted_key_function("0.0")+"|"+self.encrypted_key_function(str(random_string))+"\n")
            print("Account has been created successfully!\n")

    def deposit(self):
        while True:
            try:
                deposit = float(input("How much money do you want to deposit: "))
            except:
                print("Sorry that's not a number")
            else:
                break
        with open(self.passwords_will_save,"r") as file:
            lines = file.readlines()
        with open(self.passwords_will_save, "w") as file2:
            for x in lines:
                user,passw,money,transfer_id = x.strip("\n").split("|")
                each_user = self.decrypted_key_function(user)+"|"+self.decrypted_key_function(passw)+"|"+self.decrypted_key_function(money)+"|"+self.decrypted_key_function(transfer_id)
                after_money = self.encrypted_key_function(self.username)+"|"+self.encrypted_key_function(self.password)+"|"+self.encrypted_key_function(str(float(self.money)+float(deposit)))+"|"+self.encrypted_key_function(self.transfer_id)+"\n"
                account = self.username+"|"+self.password+"|"+str(self.money)+"|"+self.transfer_id
                if account != each_user:
                    file2.write(x)
                elif account == each_user:
                    file2.write(after_money)
                    self.money = float(self.money)+float(deposit)
                    print("Money has been deposited successfully")

    def withdraw(self):
        while True:
            try:
                withdraw = float(input("How much money do you want to withdraw: "))
            except:
                print("Sorry that's not a number")
            else:
                break
        if float(self.money) >= withdraw:
            with open(self.passwords_will_save, "r") as file:
                lines = file.readlines()
            with open(self.passwords_will_save, "w") as file2:
                for x in lines:
                    user, passw, money,transfer_id = x.strip("\n").split("|")
                    each_user = self.decrypted_key_function(user) + "|" + self.decrypted_key_function(passw) + "|" + self.decrypted_key_function(money)+"|"+self.decrypted_key_function(transfer_id)
                    after_money = self.encrypted_key_function(self.username) + "|" + self.encrypted_key_function(self.password) + "|" + self.encrypted_key_function(str(float(self.money) - float(withdraw)))+"|"+self.encrypted_key_function(self.transfer_id) + "\n"
                    account = self.username + "|" + self.password + "|" + str(self.money)+"|"+self.transfer_id
                    if account != each_user:
                        file2.write(x)
                    elif account == each_user:
                        file2.write(after_money)
                        self.money = float(self.money) - float(withdraw)
                        print("Money has been withdrawn successfully")
        else:
            print("Sorry, You have insufficient funds in your account")

    def view(self):
        print("Money:", str(float(self.money)))
        print("Transfer id:", str(self.transfer_id))

    def delete(self):
        last_chance = input("Are you sure you want to delete account (Yes/No): ")
        if last_chance.lower() == "y":
            with open(self.passwords_will_save,"r") as file:
                lines = file.readlines()
            with open(self.passwords_will_save, "w") as file2:
                for x in lines:
                    user,passw,money,transfer_id = x.strip("\n").split("|")
                    each_user = self.decrypted_key_function(user)+"|"+self.decrypted_key_function(passw)+"|"+self.decrypted_key_function(money)+"|"+self.decrypted_key_function(transfer_id)
                    account = self.username+"|"+self.password+"|"+str(self.money)+"|"+self.transfer_id
                    if account != each_user:
                        file2.write(x)
                    else:
                        print("Account Deleted\n")

    def transfer(self):
        with open(self.passwords_will_save, "r") as file:
            lines = file.readlines()

        with open(self.passwords_will_save, "w") as file2:
            id_valid = None
            verif1 = 0

            while True:
                send = input("Enter the person's transfer id or cancel the transfer by pressing (Cancel): ").strip()

                for y in lines:
                    if send.lower() == "cancel":file2.write(y)
                    elif send == self.decrypted_key_function(y.strip("\n").split("|")[3]):id_valid = self.decrypted_key_function(y.strip("\n").split("|")[3])

                if id_valid is not None:
                    break
                elif send.lower() == "cancel":
                    print("Transaction canceled\n")
                    return
                else:
                    print("Sorry, the person's transfer id is incorrect or you did not type cancel")

            while True:
                try:
                    send_money = float(input("How much money do you want to transfer to " + send + ": "))
                    last_chance = input("Are you sure you want to send " + str(send_money) + " to " + send + " (Yes/No): ")
                    if last_chance.lower().strip()[0] == "n":
                        print("Transaction successfully cancelled\n")

                    elif last_chance.lower().strip()[0] == "y":
                        break
                    else:
                        print("Sorry, you did not type yes or no")
                        continue
                except ValueError:
                    print("Sorry, that's not a valid number")
                else:
                    break

            for x in lines:
                if last_chance.lower().strip()[0] == "n":
                    file2.write(x)
                    verif1 += 1
                    continue

                receiver_user_encrypt,receiver_password_encrypt,receiver_money_encrypt,receiver_id_encrypt = x.strip("\n").split("|")

                if self.money >= send_money:
                    sender_details_after = (self.encrypted_key_function(self.username) + "|"+ self.encrypted_key_function(self.password) + "|"+ self.encrypted_key_function(str(float(self.money) - send_money)) + "|"+ self.encrypted_key_function(self.transfer_id) + "\n")
                    receiver_details_after = (receiver_user_encrypt + "|"+ receiver_password_encrypt + "|"+ self.encrypted_key_function(str(float(self.decrypted_key_function(receiver_money_encrypt)) + send_money)) + "|"+ receiver_id_encrypt + "\n")

                    if self.decrypted_key_function(receiver_id_encrypt) == self.transfer_id:file2.write(sender_details_after);self.money == float(self.money);self.money -= send_money
                    elif self.decrypted_key_function(receiver_id_encrypt) == send:file2.write(receiver_details_after)
                    else:file2.write(x)
                else:
                    if verif1 == 0:
                        print("Sorry, you have insufficient funds in your account\n")
                    verif1 += 1
                    file2.write(x)
            else:
                if verif1 == 0:
                    print("Transaction successfully completed\n")
                else:
                    return

    @staticmethod
    def logout():
        print("Logging out\n")
        time.sleep(3)
        return
