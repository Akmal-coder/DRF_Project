from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from users.models import Subscription


@shared_task
def send_course_update_email(course_id, course_title):
    """
    Асинхронная отправка уведомлений подписчикам об обновлении курса
    """
    # Получаем всех подписчиков курса
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user')

    # Собираем email'ы подписчиков
    recipient_emails = [sub.user.email for sub in subscriptions if sub.user.email]

    if not recipient_emails:
        return f"No subscribers for course {course_title}"

    # Формируем ссылку на курс
    course_url = f"{settings.SITE_URL}{reverse('course-detail', args=[course_id])}"

    # Тема и текст письма
    subject = f"Курс '{course_title}' был обновлен"
    message = f"""
    Здравствуйте!

    Курс '{course_title}', на который вы подписаны, был обновлен.

    Перейдите по ссылке, чтобы посмотреть новые материалы:
    {course_url}

    С уважением,
    Команда LMS Project
    """

    # Отправляем письма
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        return f"Sent update notifications to {len(recipient_emails)} subscribers for course {course_title}"
    except Exception as e:
        return f"Error sending notifications: {str(e)}"