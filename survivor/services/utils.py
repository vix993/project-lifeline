from rest_framework.views import exception_handler
from rest_framework import serializers

def make_set(request_dict):
    set = {}
    list_items = request_dict.split(';')
    for element in list_items:
        query_list = element.split(':')
        if len(query_list) < 2:
            return query_list
        set[query_list[0]] = query_list[1]
    return set

def check_stock(trade_items, stock_items):
    for key in trade_items:
        if int(trade_items[key]) < int(stock_items[key]):
            raise serializers.ValidationError("Please make sure both parties have stock.")