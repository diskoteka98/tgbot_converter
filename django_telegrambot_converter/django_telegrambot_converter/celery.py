import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_telegrambot_converter.settings')

app = Celery('django_telegrambot_converter')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'core.tasks.task_get_rates_from_api',
        'schedule': crontab(hour="1", minute="0"),
    },
}
