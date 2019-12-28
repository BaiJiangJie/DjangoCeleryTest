# coding: utf-8
#
from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings

__all__ = ['app']


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCeleryTest.settings')

app = Celery('DjangoCeleryTest')

# app.config_from_object('django.conf:settings')

CELERY_CONFIGS = {
    'CELERY_BROKER_URL': 'redis://localhost:6379/10',
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/11',
    'CELERY_ACCEPT_CONTENT': ['application/json'],
    'CELERY_TASK_SERIALIZER': 'json',
    'CELERY_RESULT_SERIALIZER': 'json',
    'CELERY_WORKER_MAX_TASKS_PER_CHILD': 5,
    # 'CELERY_TIMEZONE': 'Africa/Nairobi'
}


configs = {k: v for k, v in CELERY_CONFIGS.items() if k.startswith('CELERY')}

app.namespace = 'CELERY'
app.conf.update(configs)

packages = [app_config.split('.')[0] for app_config in settings.INSTALLED_APPS]
app.autodiscover_tasks(packages=packages)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
