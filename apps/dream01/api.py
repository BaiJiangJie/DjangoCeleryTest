# coding: utf-8
#


from rest_framework import generics, status, views
from rest_framework.response import Response
from .tasks import add, print_lines

__all__ = ['HelloApi', 'TaskAddApi', 'TaskRunApi']


task_name_map = {
    'add': add,
    'print_lines': print_lines,
}


class HelloApi(views.APIView):

    def get(self, request, *args, **kwargs):
        return Response({'dream': 'Hello'})


class TaskAddApi(views.APIView):

    def get(self, request, *args, **kwargs):
        task = add.delay(10, 100)
        return Response({'task': task.id})


class TaskRunApi(views.APIView):

    def run_task(self):
        task_name = self.request.query_params.get('task', 'add')
        task = task_name_map.get(task_name)
        task = task.delay()
        return task

    def get(self, request, *args, **kwargs):
        task = self.run_task()
        return Response({'task': task.id})
