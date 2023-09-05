from utils.environment import get_environment

status_opened = "opened"
status_closed = "closed"
status_paid = "paid"
status_deleted = "deleted"
status_delivered = "delivered"

# email_sender
email_sender = "ishchuka.mail.sender@gmail.com"
email_password = get_environment("EMAIL_PASSWORD")
email_receiver = "ishchuka.mail.sender@gmail.com"
subject = "Test email confirmation"
user_confirm_body = """
Please confirm you email. http://127.0.0.1:5000/user/confirm/{}/{}
"""
