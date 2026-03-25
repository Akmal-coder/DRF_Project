import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


# Настройка периодических задач
app.conf.beat_schedule = {
    'block-inactive-users-daily': {
        'task': 'users.tasks.block_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # Каждый день в полночь
        'options': {
            'expires': 3600,  # Задача перестает быть актуальной через час
        }
    },
    'test-beat-every-minute': {
        'task': 'users.tasks.test_beat_task',
        'schedule': crontab(minute='*/1'),  # Каждую минуту для теста
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')