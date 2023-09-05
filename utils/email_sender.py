import smtplib
import ssl
from email.message import EmailMessage

from constants import email_sender, subject, email_password


def mail_sender(email_receiver, body):
    email_message = EmailMessage()
    email_message["From"] = email_sender
    email_message["To"] = email_receiver
    email_message["Subject"] = subject
    email_message.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email_message.as_string())
