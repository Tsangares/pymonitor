import smtplib,ssl,os,getpass
server = "smtp.gmail.com"
port=587
email = input("Enter email: ")
fromEmail = email
toEmail = email
password = getpass.getpass("email password: ")
context = ssl.create_default_context()
with smtplib.SMTP(server,port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.login(fromEmail, password)
    if not os.path.isfile("email.txt"):
        open('email.txt','w+').write("")
        print("Made email.txt, please put email there.")
        quit(1)
    message = open('email.txt').read()
    server.sendmail(fromEmail,toEmail,message)
print("Sent")
