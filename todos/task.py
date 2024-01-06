from celery import shared_task
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger("celery_task")

@shared_task
def my_task(arg1, arg2):
    # Task logic here
    result = arg1 + arg2
    print(f"-----------------------------------Result: {result}-----------------------------------------")
    return result

@shared_task
def send_email(subject: str, body: str, receiver_email: list, cc: list = []):
    try:
        email = EmailMessage(subject=subject, body=body, to=receiver_email, cc=cc)
        email.send()
        logger.info(f"Successfully sent email to user: {receiver_email}")

        return f"Successfully sent email to user: {receiver_email}."
    except Exception as e:
        logger.error(f"Failed to send email for user: {receiver_email}, with Exception - {type(e).__name__}, with Arguments: {e.args}")
        return f"Fail to send Email to user: {receiver_email}"