from django.http import HttpResponse
from django.db.models import Q

from rest_framework import generics, serializers, mixins

from survivor.serializers import CreateSurvivorSerializer, SurvivorRetreiveUpdateSerializer
from survivor.models import Survivor
from survivor.validators import Validation

# Create new survivor and retrieve all of the current ones
# query individuals

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
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(status=400, content=e)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

# Update survivor current position (lat, long)
# Get individuals

class RetrieveUpdateSurvivorView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = SurvivorRetreiveUpdateSerializer

    def get_queryset(self):
        return Survivor.objects.all()
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}