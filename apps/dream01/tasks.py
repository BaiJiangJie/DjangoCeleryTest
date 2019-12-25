# coding: utf-8
#

import random
import time
from celery import shared_task

__all__ = ['add', 'print_lines']


@shared_task
def add():
    return 2000 + 20


@shared_task
def print_lines():
    for i in range(10000):
        time.sleep(random.randint(0, 10))
        print('{}. line'.format(i))

