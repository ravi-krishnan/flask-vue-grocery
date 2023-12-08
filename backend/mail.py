from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_PORT=1025
SMTP_HOST="localhost"
SENDER_EMAIL="dummy@gmail.com"
SENDER_PASSWORD=""


def send_message(to,subject,content_body):
    msg=MIMEMultipart()
    msg['To']= to
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg.attach(MIMEText(content_body,'html'))
    server = SMTP(host=SMTP_HOST,port=SMTP_PORT)
    server.send_message(msg=msg)
    server.quit()

