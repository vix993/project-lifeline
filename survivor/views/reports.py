from django.http import HttpResponse

from rest_framework import generics, serializers

from survivor.serializers import ReportsSerializer
from survivor.models import Survivor, Reports
from survivor.validators import Validation

from survivor.services.report import ReportService

# Retrieve an up-to-date report of the situation
# Items lost due to infection, and value of these items.

class ReportsView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = ReportsSerializer

    def get_object(self):
        qs = ReportService().do_report()
        return qs