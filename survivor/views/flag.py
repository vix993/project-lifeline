from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import generics, serializers, mixins
from rest_framework.decorators import api_view

from survivor.serializers import CreateSurvivorSerializer, SurvivorRetreiveUpdateSerializer, FlagAsInfectedSerializer, TradeItemSerializer, ReportsSerializer
from survivor.models import Survivor, FlagAsInfected, Reports
from survivor.validators import Validation

from survivor.services.flag_as_infected import do_flag_as_infected
from survivor.services.utils import make_set

# A survivor can flag another once. Occurences
# are stored for validation and reporting

class CreateFlagAPIView(mixins.RetrieveModelMixin, generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = FlagAsInfectedSerializer

    def get_queryset(self):
        return FlagAsInfected.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            do_flag_as_infected(request)
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(status=400, content=e)