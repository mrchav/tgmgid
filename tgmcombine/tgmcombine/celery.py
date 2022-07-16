import os
from celery import Celery
from celery.schedules import crontab

#import tgmcombine.s

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tgmcombine.settings')

app = Celery('tgmcombine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'star_parser': {
        'task': 'parser.tasks.star_parser',
        'schedule': crontab(hour="*/24"),
    }
}