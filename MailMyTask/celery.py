
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from MailMyTask.settings import CELERY_BROKER_URL

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MailMyTask.settings')

app = Celery('MailMyTask')  # Replace 'your_project' with your project's name.

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_transport_options = {'visibility_timeout': 31536000}
app.conf.result_backend_transport_options = {'visibility_timeout': 31536000}
app.conf.visibility_timeout = 31536000

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)