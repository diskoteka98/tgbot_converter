from typing import Any

import requests
import datetime
import sqlite3
from django.conf import settings
from core.models import Rate
from decimal import Decimal


def get_rates_from_api(currency_from):
    response = requests.get(
        f"https://api.freecurrencyapi.com/v1/latest?apikey={settings.API_KEY}&base_currency={currency_from}")
    print(response.json())
    rates = response.json()["data"]
    print("zapros")
    return rates


def save_rates_to_db(rates, currency_from):
    date = datetime.date.today()

    new_rates = []
    for currency_to, rate in rates.items():
        new_rates.append(
            Rate(
                currency_from=currency_from,
                currency_to=currency_to,
                date=date,
                rate=Decimal(rate)
            )
        )

    Rate.objects.bulk_create(new_rates)


def get_rate_from_db(currency_from: str, currency_to: str) -> Decimal | None:

    date = datetime.date.today()
    try:
        rate = Rate.objects.get(currency_from=currency_from, currency_to=currency_to, date=date)
    except Rate.DoesNotExist:
        return None
    return rate.rate


def convert(currency_from, currency_to, amount):
    currency_from = str(currency_from).upper()
    currency_to = str(currency_to).upper()
    rate = get_rate_from_db(currency_from, currency_to)
    if not rate:
        rates = get_rates_from_api(currency_from)
        save_rates_to_db(rates, currency_from)
        rate = rates[currency_to]
    return amount * rate



