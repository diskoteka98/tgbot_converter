from typing import Any

import requests
import datetime
import sqlite3
from django.conf import settings
from core.models import Rate, Currency
from decimal import Decimal


def get_rates_from_api(currency_from):
    response = requests.get(
        f"https://api.freecurrencyapi.com/v1/latest?apikey={settings.API_KEY}&base_currency={currency_from}")
    response.raise_for_status()
    print(response.json())
    rates = response.json()["data"]
    print("zapros")
    return rates


def save_rates_to_db(rates, currency_from_name):
    date = datetime.date.today()

    currency_from = Currency.objects.get(name=currency_from_name)

    new_rates = []
    for currency_to_name, rate in rates.items():
        currency_to, created = Currency.objects.get_or_create(name=currency_to_name)


        new_rates.append(
            Rate(
                currency_from=currency_from,
                currency_to=currency_to,
                date=date,
                rate=Decimal(rate)
            )
        )

    if new_rates:
        Rate.objects.bulk_create(new_rates)
        print(f"Successfully saved {len(new_rates)} rates to the database.")


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
        raise Exception("ваня уехал на дачу")

    return amount * rate


print('hello ')

print('hello')

