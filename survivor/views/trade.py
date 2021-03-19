from django.http import HttpResponse

from rest_framework import generics, serializers, mixins

from survivor.serializers import TradeItemSerializer
from survivor.models import TradeItem

from survivor.services.trade import get_item_sets_and_check_if_infected, get_stocks, validate_stock,\
    get_trade_values, build_new_trader_stocks
from survivor.services.utils import make_set

class CreateItemTradeAPIView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = TradeItemSerializer
    def get_queryset(self):
        qs = TradeItem.objects.all()
        return qs

    def post(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            return HttpResponse(status=400, content=e)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}