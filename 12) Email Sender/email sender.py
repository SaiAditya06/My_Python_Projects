import smtplib
import getpass


def mail():
    domain = input("What mail hosting server domain (do not include suffix): ")
    extension = input("What is the suffix of the domains (do not include domain): ")
    hosting = "smtp.{d}.{e}".format(d=domain,e=extension).lower()
    try:
        smtp = smtplib.SMTP(hosting)
    except:
        print("There was an error please type the right mail hosting server domain and suffix of the domain\n\n\n")
    else:
        if smtp.ehlo()[0] == 250 and smtp.starttls()[0] == 220:
            if hosting == "smtp.gmail.com":
                email = input("Enter Senders Email: ").lower()
                password = getpass.getpass("Enter Senders App Password (note: what you are typing will not be visible): ")
                try:
                    smtp.login(email,password)
                except:
                    print("The email or password might be incorrect\n\n\n")
                else:
                    if smtp.login(email,password)[0] == 503:
                        from_email = email
                        to_email = input("Enter Receivers Email: ").lower()
                        subject = input("Enter the Subject: ")
                        message = input("Enter the message: ")
                        msg = "Subject: {s}\n\n{m}".format(s=subject,m=message)
                        smtp.sendmail(from_email,to_email,msg)
                        print("\n\n")
                    else:
                        pass
            elif hosting != "smtp.gmail.com":
                email = input("Enter Senders Email: ").lower()
                password = getpass.getpass("Enter Senders Password (note: what you are typing will not be visible): ")
                try:
                    smtp.login(email,password)
                except:
                    print("The email or password might be incorrect\n\n\n")
                else:
                    if smtp.login(email,password)[0] == 503:
                        from_email = email
                        to_email = input("Enter Receivers Email: ").lower()
                        subject = input("Enter the Subject: ")
                        message = input("Enter the message: ")
                        msg = "Subject: {s}\n\n{m}".format(s=subject,m=message)
                        smtp.sendmail(from_email,to_email,msg)
                        print("Message has been sent, Now you can send another mail\n\n\n")
                    else:
                        pass
            else:
                pass
        else:
            pass


while True:
    mail()
