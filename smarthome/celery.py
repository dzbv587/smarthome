import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarthome.settings')

app = Celery('smarthome')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'windows-schedule': {
        'task': 'home.tasks.sync_windows',
        'schedule': timedelta(seconds=5),
    },
    'sensors-schedule': {
        'task': 'home.tasks.sync_sensors',
        'schedule': timedelta(seconds=5),
    },
    'lights-schedule': {
        'task': 'home.tasks.sync_lights',
        'schedule': timedelta(seconds=5),
    },
    'switchs-schedule': {
        'task': 'home.tasks.sync_switchs',
        'schedule': timedelta(seconds=5),
    },
    'fans-schedule': {
        'task': 'home.tasks.sync_fans',
        'schedule': timedelta(seconds=5),
    },
    'curtains-schedule': {
        'task': 'home.tasks.sync_curtains',
        'schedule': timedelta(seconds=5),
    },
}
