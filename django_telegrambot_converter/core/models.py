from datetime import datetime
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.db import models


class User(models.Model):
    telegram_id = models.PositiveIntegerField(verbose_name="ID пользователя", unique=True)
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name='Имя пользователя ')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.username} ({self.telegram_id})"


class Message(models.Model):
    profile = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name="Профиль")
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(verbose_name="Время получения", auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Сообщения {self.pk} от {self.profile}"


class Rate(models.Model):
    date = models.DateField()
    currency_from = models.CharField(max_length=3)
    currency_to = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        unique_together = ('currency_from', 'currency_to', 'date')

    def __str__(self):
        return f"{self.currency_from} to {self.currency_to} on {self.date}: {self.rate}"




