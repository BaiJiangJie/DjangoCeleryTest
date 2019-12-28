# coding: utf-8
#

import json

from django.utils.timezone import get_current_timezone
from django.db.utils import ProgrammingError, OperationalError
from django_celery_beat.models import (
    PeriodicTask, IntervalSchedule, CrontabSchedule, PeriodicTasks
)

__all__ = ['create_or_update_celery_periodic_tasks']


def create_or_update_celery_periodic_tasks(tasks):
    for name, detail in tasks.items():
        interval = None
        crontab = None
        try:
            IntervalSchedule.objects.all().count()
        except (ProgrammingError, OperationalError):
            return None

        if isinstance(detail.get("interval"), int):
            kwargs = dict(
                every=detail['interval'],
                period=IntervalSchedule.SECONDS,
            )
            # 不能使用 get_or_create，因为可能会有多个
            interval = IntervalSchedule.objects.filter(**kwargs).first()
            if interval is None:
                interval = IntervalSchedule.objects.create(**kwargs)
        elif isinstance(detail.get("crontab"), str):
            try:
                minute, hour, day, month, week = detail["crontab"].split()
            except ValueError:
                return
            kwargs = dict(
                minute=minute, hour=hour, day_of_week=week,
                day_of_month=day, month_of_year=month, timezone=get_current_timezone()
            )
            crontab = CrontabSchedule.objects.filter(**kwargs).first()
            if crontab is None:
                crontab = CrontabSchedule.objects.create(**kwargs)
        else:
            return

        defaults = dict(
            interval=interval,
            crontab=crontab,
            name=name,
            task=detail['task'],
            args=json.dumps(detail.get('args', [])),
            kwargs=json.dumps(detail.get('kwargs', {})),
            description=detail.get('description') or ''
        )
        task = PeriodicTask.objects.update_or_create(
            defaults=defaults, name=name,
        )
        PeriodicTasks.update_changed()
        return task
