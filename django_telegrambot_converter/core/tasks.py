from celery import shared_task
from core.converter import get_rates_from_api, save_rates_to_db
from core.models import Currency


@shared_task
def task_get_rates_from_api(currency_name=None):

    currencies = Currency.objects.filter(name=currency_name) if currency_name else Currency.objects.all()

    print(f"Запуск фоновой задачи для обновления курсов валют: {', '.join([c.name for c in currencies])}")

    for currency in currencies:
        rates = get_rates_from_api(currency.name)
        save_rates_to_db(rates, currency.name)
        print(f"Курсы валют для {currency.name} успешно обновлены")


