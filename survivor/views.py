from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import generics, serializers, mixins
from rest_framework.decorators import api_view

from .serializers import CreateSurvivorSerializer, SurvivorRetreiveUpdateSerializer, FlagAsInfectedSerializer, TradeItemSerializer
from .models import Survivor

from .services.flag_as_infected import do_flag_as_infected
from .services.trade import get_item_sets_and_check_if_infected, get_stocks, validate_stock,\
    get_trade_values, build_new_trader_stocks
# import sys
# sys.path.append('../')



@api_view(['GET'])
def health_check(request):
    return HttpResponse(status=200)

# We are using the generic API views from the django rest framework documentation
# https://www.django-rest-framework.org/api-guide/generic-views/

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
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(status=400, content=e)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class RetrieveUpdateSurvivorView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = SurvivorRetreiveUpdateSerializer

    def get_queryset(self):
        return Survivor.objects.all()
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class CreateFlagAPIView(mixins.RetrieveModelMixin, generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = FlagAsInfectedSerializer

    def get_queryset(self):
        return FlagAsInfected.objects.all()

    def post(self, request, *args, **kwargs):
        do_flag_as_infected(request)
        return self.create(request, *args, **kwargs)

class CreateItemTradeAPIView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = TradeItemSerializer
    def get_queryset(self):
        qs = TradeItem.objects.all()
        return qs

    def post(self, request, *args, **kwargs):
        payload = request.data
        buyer_item_set, seller_item_set = get_item_sets_and_check_if_infected(payload)
        
        buyer_current_items, seller_current_items,\
        buyer_offered_items, seller_requested_items = get_stocks(buyer_item_set, seller_item_set, payload)
        validate_stock(buyer_current_items, seller_current_items, buyer_offered_items, seller_requested_items)
        sum_buy_value, sum_sell_value = get_trade_values(buyer_offered_items, seller_requested_items)
        if sum_buy_value == sum_sell_value:
            buyer_post_transaction, seller_post_transaction = build_new_trader_stocks(buyer_current_items, seller_requested_items,\
                buyer_offered_items, seller_current_items)
        
            buyer_item_set.items = buyer_post_transaction[:len(buyer_post_transaction) - 1]
            seller_item_set.items = seller_post_transaction[:len(seller_post_transaction) - 1]
            buyer_item_set.save()
            seller_item_set.save()
        else:
            raise serializers.ValidationError('Uneven trade values are not allowed')
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}