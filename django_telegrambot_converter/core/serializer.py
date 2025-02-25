from rest_framework import serializers
from .models import Currency, Rate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'symbol']


class RateSerializer(serializers.ModelSerializer):
    currency_from = CurrencySerializer()
    currency_to = CurrencySerializer()

    class Meta:
        model = Rate
        fields = ['currency_from', 'currency_to', 'rate', 'date']