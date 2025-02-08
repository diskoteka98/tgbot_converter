from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Currency
from .tasks import task_get_rates_from_api


@receiver(post_save, sender=Currency)
def update_currency_rate(sender, instance, created, **kwargs):
    if created:
        task_get_rates_from_api.delay(instance.name)