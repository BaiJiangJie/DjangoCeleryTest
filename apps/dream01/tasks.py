# coding: utf-8
#

import random
import time
from celery import shared_task, current_task
from fly.utils import create_or_update_celery_periodic_tasks

__all__ = ['add', 'print_lines']


@shared_task
def add():
    return 2000 + 20


@shared_task
def print_lines():
    for i in range(10000):
        time.sleep(random.randint(0, 10))
        print('{}. line'.format(i))


# test celery issue (Bai)

from celery import shared_task
import random


@shared_task(soft_time_limit=5)
def long_time_task():
    r = random.random()
    print("Task running long ===>>>: {}".format(random.random()))


@shared_task
def short_time_task():
    print("Task running short ===>>>: {}".format(random.random()))


@shared_task
def mid_time_task():

    print("Task running mid ===>>>: {}".format(random.random()))

@shared_task
def raise_exception_attribute():
    raise AttributeError(current_task.request.id)


@shared_task
def raise_exception_syntax():
    raise SyntaxError(current_task.request.id)


def perform_long_time_task():
    task = long_time_task.delay()
    return task


def perform_short_time_task():
    task = short_time_task.delay()
    return task


def perform_mid_time_task():
    task = mid_time_task.delay()
    return task


def perform_raise_attribute():
    return raise_exception_attribute.delay()


def perform_raise_syntax():
    return raise_exception_syntax.delay()


def create_celery_task(num=10):
    task_list = [
        perform_long_time_task,
        perform_short_time_task,
        perform_mid_time_task,
        perform_raise_attribute,
        perform_raise_syntax
    ]
    for i in range(num):
        print("Total: {}. Creating task is: {}th".format(num, i))
        index = random.randint(0, len(task_list)-1)
        task = task_list[index]()
        print('==============>: {}'.format(task))


@shared_task
def periodic_task_1():
    for i in range(3):
        time.sleep(2)
        print('{}. periodic_task_1'.format(i))


def create_periodic_task_1():
    tasks = {
        'check_password_expired_periodic': {
            'task': periodic_task_1.name,
            'interval': 10,
            'enabled': True,
        }
    }
    create_or_update_celery_periodic_tasks(tasks)


# create_periodic_task_1()


