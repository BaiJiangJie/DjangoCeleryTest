# coding: utf-8
#
from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings

__all__ = ['app']


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCeleryTest.settings')

app = Celery('DjangoCeleryTest')

app.config_from_object('django.conf:settings')

packages = [app_config.split('.')[0] for app_config in settings.INSTALLED_APPS]
app.autodiscover_tasks(packages=packages)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
