from django.urls import path
from .views import CurrencyList, RateList

urlpatterns = [
    path('currencies/currencies/', CurrencyList.as_view(), name='currency-list'),
    path('rates/', RateList.as_view(), name='rate-list'),
]