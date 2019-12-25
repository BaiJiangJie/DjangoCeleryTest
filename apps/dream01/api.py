# coding: utf-8
#


from rest_framework import generics, status, views
from rest_framework.response import Response

__all__ = ['HelloApi']


class HelloApi(views.APIView):

    def get(self, request, *args, **kwargs):
        response = Response(data={'dream': 'Hello'}, status=status.HTTP_200_OK)
        return response
