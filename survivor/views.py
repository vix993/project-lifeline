from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics, serializers
from rest_framework.decorators import api_view


@api_view(['GET'])
def health_check(request):
    return HttpResponse(status=200)