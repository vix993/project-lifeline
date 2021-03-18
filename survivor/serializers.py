from rest_framework import serializers

from survivor.models import Survivor, FlagAsInfected, TradeItem

class CreateSurvivorSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Survivor
        fields = [
            'url',
            'name',
            'age',
            'gender',
            'latitude',
            'longitude',
            'items',
            'infected',
            'infection_marks',
        ]
        read_only_fields = ['infected']
    infection_marks = serializers.HiddenField(default=0)

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_name(self, value):
        qs = Survivor.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Name must be unique, we cannot risk confusing id's")
        return value

class SurvivorRetreiveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = [
            'name',
            'age',
            'gender',
            'latitude',
            'longitude',
            'items',
            'infected',
            'infection_marks',
        ]
        read_only_fields = [
            'infected',
            'name',
            'age',
            'gender',
            'items',
            'infected',
            'infection_marks',
        ]

class FlagAsInfectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlagAsInfected
        fields = [
            'pk',
            'flaged_pk',
            'flager_pk'
        ]

        def get_url(self, obj):
            request = self.context.get("request")
            return obj.get_api_url(request=request)

class TradeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeItem
        fields = [
            'seller_pk',
            'buyer_pk',
            'offered_items',
            'requested_items',
        ]