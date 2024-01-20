import logging
from datetime import datetime, timedelta, timezone
from django.db import models

from MailMyTask import settings
from MailMyTask.common_detail import SUBJECT, EMAIL_BODY
from todos.task import send_email
from MailMyTask.celery import app

# Logger
logger = logging.getLogger("django")

class Folder(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class SubFolder(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField(blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField(blank=True)
    completion_time = models.DateTimeField(null=True)
    reminder = models.BooleanField(default=False)
    reminder_before_time = models.IntegerField(null=True)
    celery_task_id = models.CharField(blank=True, max_length=220)
    task_priority = models.ForeignKey(
        "TaskPriority", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_folder = models.ForeignKey(
        SubFolder, on_delete=models.SET_NULL, null=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def update_schedule_email(self) -> None:

        if self.celery_task_id:
            logger.info(f"Revoking the task with ID: {self.celery_task_id}")
            app.control.revoke(self.celery_task_id, terminate=True)
            # Reschedule the task with new detail.
            self.schedule_email()
        

    def schedule_email(self) -> None:
        try:
            date_time_obj: datetime = self.completion_time
            reminder_before_time = self.reminder_before_time

            if not date_time_obj:
                logger.warning("Completion time is not provided to schedule email.")
                return
            
            if not reminder_before_time:
                reminder_before_time = 0

            reminder_time: datetime = date_time_obj - timedelta(minutes=int(reminder_before_time))
            # reminder time should not be lower then current datetime, if it is then sent email after 10 seconds after current datetime.
            time_diff = reminder_time - datetime.now(timezone.utc)
            if not ((time_diff.days > 0) or (time_diff.seconds > 0) or (time_diff.minutes > 0)):
                reminder_time = datetime.now(
                    timezone.utl) + timedelta(seconds=20)

            subject = SUBJECT.format(task_name=self.title)
            email_body = EMAIL_BODY.format(task_name=self.title, due_date=self.completion_time if self.completion_time else "--",
                priority=self.task_priority if self.task_priority else "--", status="Due"
                )

            # adding task in queue for celery.
            self.celery_task_id = send_email.apply_async(args=[subject, email_body, ['singharunendra978@gmail.com']], eta=reminder_time)
            self.save()

            # Saving task id in DB
        except Exception as e:
            logger.error(
                f"Process failed with Exception: {type(e).__name__}, with Exception: {e.args}", stack_info=True, exc_info=True)

    def __str__(self) -> str:
        return self.title


class TaskPriority(models.Model):
    title = models.CharField(max_length=90)
    color = models.CharField(max_length=20)
    weight = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
