from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import generics, serializers, mixins
from rest_framework.decorators import api_view

from .serializers import CreateSurvivorSerializer, SurvivorRetreiveUpdateSerializer, FlagAsInfectedSerializer, TradeItemSerializer, ReportsSerializer
from .models import Survivor, FlagAsInfected, Reports
from .validators import Validation

from .services.flag_as_infected import do_flag_as_infected
from .services.trade import get_item_sets_and_check_if_infected, get_stocks, validate_stock,\
    get_trade_values, build_new_trader_stocks
from .services.utils import make_set

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

class ReportsView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = ReportsSerializer
    def get_object(self):
        if not Reports.objects.all():
            Reports.objects.create(
                percentage_infected='', percentage_healthy='', average_water='', average_soup='',
                average_pouch='', average_ak47='', points_lost=''
            )
        infected = 0
        healthy = 0
        qs = Survivor.objects.all()
        qs1 = Reports.objects.first()
        lost_points = 0
        fiji_water = 0
        campbell_soup = 0
        first_aid_pouch = 0
        ak47 = 0
        for element in qs:
            if element.infected:
                infected_set = make_set(element.items)
                for key in infected_set:
                    lost_points = lost_points + (int(infected_set[key]) * int(Validation().price_dict[key]))
                    if key == 'Fiji Water':
                        fiji_water += int(infected_set[key])
                    if key == 'Campbell Soup':
                        campbell_soup += int(infected_set[key])
                    if key == 'First Aid Pouch':
                        first_aid_pouch += int(infected_set[key])
                    if key == 'AK47':
                        ak47 += int(infected_set[key])
                infected += 1
            else:
                healthy += 1
                healthy_set = make_set(element.items)
                for key in healthy_set:
                    if key == 'Fiji Water':
                        fiji_water += int(healthy_set[key])
                    if key == 'Campbell Soup':
                        campbell_soup += int(healthy_set[key])
                    if key == 'First Aid Pouch':
                        first_aid_pouch += int(healthy_set[key])
                    if key == 'AK47':
                        ak47 += int(healthy_set[key])
        survivor_count = infected + healthy
        qs1.percentage_infected = '{:.2f}%'.format((infected / survivor_count) * 100)
        qs1.percentage_healthy = '{:.2f}%'.format((healthy / survivor_count) * 100)
        qs1.average_water = '{:.2f} Fiji Waters per survivor.'.format(fiji_water / survivor_count)
        qs1.average_soup = '{:.2f} Campbell Soups per survivor.'.format(campbell_soup / survivor_count)
        qs1.average_pouch = '{:.2f} First Aid Pouches per survivor.'.format(first_aid_pouch / survivor_count)
        qs1.average_ak47 = "{:.2f} AK47's per survivor.".format(ak47 / survivor_count)
        qs1.points_lost = "{} points lost due to owner infection.".format(lost_points)
        qs1.save()
        return qs1