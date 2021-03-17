from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics, serializers, mixins
from rest_framework.decorators import api_view

from .serializers import CreateSurvivorSerializer, SurvivorRetreiveUpdateSerializer
from .models import Survivor


@api_view(['GET'])
def health_check(request):
    return HttpResponse(status=200)

# Create and query Survivors from list

class CreateSurvivorAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = CreateSurvivorSerializer

    def get_queryset(self):
        qs = Survivor.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(name__icontains=query)|
                           Q(age__icontains=query)
                           ).order_by('-age')
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class RetrieveUpdateSurvivorView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = SurvivorRetreiveUpdateSerializer

    def get_queryset(self):
        return Survivor.objects.all()
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}