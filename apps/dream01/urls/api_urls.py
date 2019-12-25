# coding: utf-8
#

from django.urls import path
from .. import api

app_name = 'dream01'

__all__ = []


urlpatterns = [
    path('hello/', api.HelloApi.as_view(), name='hello'),
]
