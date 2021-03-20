from survivor.models import Survivor
from survivor.validators import Validation
from rest_framework import serializers

from .utils import check_stock, make_set

# Class will execute the trade validation and perform updates

class TradeService:
    def do_trade(self, payload):
        buyer_item_set, seller_item_set = self.get_item_sets_and_check_if_infected(payload)
        
        buyer_current_items, seller_current_items,\
        buyer_offered_items, seller_requested_items = self.get_stocks(buyer_item_set, seller_item_set, payload)
        self.validate_stock(buyer_current_items, seller_current_items, buyer_offered_items, seller_requested_items)
        sum_buy_value, sum_sell_value = self.get_trade_values(buyer_offered_items, seller_requested_items)
        if sum_buy_value == sum_sell_value:
            buyer_post_transaction, seller_post_transaction = self.build_new_trader_stocks(buyer_current_items, seller_requested_items,\
                buyer_offered_items, seller_current_items)
        
            buyer_item_set.items = buyer_post_transaction[:len(buyer_post_transaction) - 1]
            seller_item_set.items = seller_post_transaction[:len(seller_post_transaction) - 1]
            buyer_item_set.save()
            seller_item_set.save()
        else:
            raise serializers.ValidationError('Uneven trade values are not allowed')

    def get_item_sets_and_check_if_infected(self, payload):
        buyer_item_set = Survivor.objects.get(pk=int(payload['buyer_pk']))
        seller_item_set = Survivor.objects.get(pk=int(payload['seller_pk']))
        if seller_item_set.infected or buyer_item_set.infected:
            raise serializers.ValidationError('One of the parties is infected')
        return (buyer_item_set, seller_item_set)

    def get_stocks(self, buyer_item_set, seller_item_set, payload):
        buyer_current_items = make_set(buyer_item_set.items)
        seller_current_items = make_set(seller_item_set.items)
        buyer_offered_items = make_set(payload['offered_items'])
        seller_requested_items = make_set(payload['requested_items'])
        return (buyer_current_items, seller_current_items, buyer_offered_items, seller_requested_items)

    def validate_stock(self, buyer_current_items, seller_current_items, buyer_offered_items, seller_requested_items):
        check_stock(buyer_current_items, buyer_offered_items)
        check_stock(seller_current_items, seller_requested_items)
        for key in buyer_current_items:
            if int(buyer_current_items[key]) < int(buyer_offered_items[key]):
                raise serializers.ValidationError('You do not have your claimed resources.')
        for key in seller_current_items:
            if int(seller_current_items[key]) < int(seller_requested_items[key]):
                raise serializers.ValidationError("Try someone who has what you're requesting.")
        
    def get_trade_values(self, buyer_offered_items, seller_requested_items):
        sum_buy_value = 0;
        sum_sell_value = 0;
        for key in buyer_offered_items:
            sum_buy_value = sum_buy_value + (int(buyer_offered_items[key]) * int(Validation().price_dict[key]))
            sum_sell_value = sum_sell_value + (int(seller_requested_items[key]) * int(Validation().price_dict[key]))
        return (sum_buy_value, sum_sell_value)

    def build_new_trader_stocks(self, buyer_current_items, seller_requested_items,\
                buyer_offered_items, seller_current_items):
        buyer_post_transaction = ""
        seller_post_transaction = ""
        for key in buyer_current_items:
            buyer_post_transaction = buyer_post_transaction + key + ':{};'.format(
                str(int(buyer_current_items[key])
                    + int(seller_requested_items[key]) - int(buyer_offered_items[key]))
            )
            seller_post_transaction = seller_post_transaction + key + ':{};'.format(
                str(int(seller_current_items[key])
                    - int(seller_requested_items[key]) + int(buyer_offered_items[key]))
            )
        return (buyer_post_transaction, seller_post_transaction)

