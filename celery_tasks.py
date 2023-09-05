from celery import Celery

from utils.email_sender import mail_sender

celery = Celery('celery_task', broker='pyamqp://guest@rabbit_mq//')
# celery = Celery('celery_task', broker='pyamqp://guest@localhost//')


@celery.task
def send_email(email_receiver, body):
    mail_sender(email_receiver, body)
    print("Hello celery")
