import requests
import datetime
import sqlite3
from django.conf import settings


def get_rate_from_db(currency_from, currency_to):

    date = datetime.date.today()
    conn = sqlite3.connect("converter.sql")
    cur = conn.cursor()
    cur.execute("SELECT rate FROM rates WHERE currency_from = ? and currency_to = ? and date = ?", (currency_from, currency_to, date))
    row = cur.fetchone()
    if row is None:
        return None
    print("db_work")
    return row[0]


def save_rates_to_db(rates, currency_from):
    date = datetime.date.today()
    conn = sqlite3.connect("converter.sql")
    cur = conn.cursor()
    new_rows = []
    for currency_to in rates:
        new_rows.append([currency_to, currency_from, str(date), rates[currency_to]])

    cur.executemany("INSERT INTO rates (currency_to, currency_from, date, rate) VALUES ( ?, ?, ?, ?)", new_rows)
    conn.commit()
    cur.close()
    conn.close()


def get_rates_from_api(currency_from):
    response = requests.get(
        f"https://api.freecurrencyapi.com/v1/latest?apikey={settings.API_KEY}&base_currency={currency_from}")
    print(response.json())
    rates = response.json()["data"]
    print("zapros")
    return rates


def convert(currency_from, currency_to, amount):
    currency_from = str(currency_from).upper()
    currency_to = str(currency_to).upper()
    rate = get_rate_from_db(currency_from, currency_to)
    if not rate:
        rates = get_rates_from_api(currency_from)
        rate = rates[currency_to]
    return amount * rate

amount = 0

