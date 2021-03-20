from django.http import HttpResponse

from rest_framework.decorators import api_view

# Testing if server is running

@api_view(['GET'])
def health_check(request):
    return HttpResponse(status=200)
