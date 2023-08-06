from smtplib import SMTP
from email.message import EmailMessage
class GmailMessage:
    body=""
    subject=""
    def __init__(self,sender,password,reciever,subject="",body=""):
        self.sender=sender
        self.password=password
        self.reciever=reciever
        self.body=body
        self.subject=subject
    def sendmail(self):
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        self.msg=EmailMessage()
        self.msg['To']=self.reciever
        self.msg['From']=self.sender
        self.msg['Subject']=self.subject
        self.msg.set_content(self.body)
        server.send_message(self.msg)

class OutlookMessage:
    body=""
    subject=""
    def __init__(self,sender,password,reciever,subject="",body=""):
        self.sender=sender
        self.password=password
        self.reciever=reciever
        self.body=body
        self.subject=subject
    def sendmail(self):
        server = SMTP('smtp.outlook.com')
        server.starttls()
        server.login(self.sender, self.password)
        self.msg = EmailMessage()
        self.msg['To'] = self.reciever
        self.msg['From'] = self.sender
        self.msg['Subject'] = self.subject
        self.msg.set_content(self.body)
        server.send_message(self.msg)

