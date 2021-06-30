from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ardhi.settings')

app = Celery('ardhi')


app.conf.update(timezone='Africa/Nairobi')

app.config_from_object(settings, namespace='CELERY')

# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
