import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fashionWebsite.settings")

app = Celery('fashionWebsite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

