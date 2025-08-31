import os
from celery import Celery

# Set default Django settings module for 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

# Create Celery app instance
app = Celery('crm')

# Load settings from Django settings file using CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django app configs
app.autodiscover_tasks()
