

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Currency, Rate
from core.serializer import CurrencySerializer, RateSerializer
from .permissions import IsRaman


class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsRaman ,]


class RateList(generics.ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsRaman, ]