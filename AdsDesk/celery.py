import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AdsDesk.settings')

app = Celery('AdsDesk')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_ads_every_monday_8am': {
        'task': 'Desk.tasks.send_weekly_ads',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}