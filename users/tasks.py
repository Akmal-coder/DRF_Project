from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User
import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца
    """
    # Вычисляем дату месяц назад
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим активных пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=one_month_ago
    ).exclude(is_superuser=True)

    count = inactive_users.count()

    if count > 0:
        # Блокируем найденных пользователей
        inactive_users.update(is_active=False)
        return f"Блокировано {count} неактивных пользователей"
    else:
        return "Неактивных пользователей не найдено"


@shared_task
def test_beat_task():
    """
    Тестовая задача для проверки работы celery-beat
    """
    print("Celery-beat работает!")
    return "Celery-beat тест выполнен"