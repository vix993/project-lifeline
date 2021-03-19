from django.contrib import admin

from .models import Survivor, FlagAsInfected, Reports, TradeItem

admin.site.register(Survivor)
admin.site.register(FlagAsInfected)
admin.site.register(TradeItem)
admin.site.register(Reports)

