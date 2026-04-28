import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULES', 'wapi.settings')

app = Celery('wapi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()