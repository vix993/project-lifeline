from django.http import HttpResponse

from rest_framework import generics, serializers, mixins

from survivor.serializers import TradeItemSerializer
from survivor.models import TradeItem

from survivor.services.trade import TradeService
from survivor.services.utils import make_set

class CreateItemTradeAPIView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = TradeItemSerializer
    def get_queryset(self):
        qs = TradeItem.objects.all()
        return qs

    def post(self, request, *args, **kwargs):
        try:
            TradeService().do_trade(request.data)
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(status=400, content=e)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}