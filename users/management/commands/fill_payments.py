from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User, Payment
from materials.models import Course, Lesson
from decimal import Decimal
import random


class Command(BaseCommand):
    """Кастомная команда для заполнения базы тестовыми платежами"""
    help = 'Заполняет таблицу платежей тестовыми данными'

    def handle(self, *args, **options):
        # Очищаем существующие платежи
        Payment.objects.all().delete()

        # Получаем всех пользователей
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('Нет пользователей в базе. Сначала создайте пользователей.'))
            return

        # Получаем все курсы и уроки
        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not courses and not lessons:
            self.stdout.write(self.style.ERROR('Нет курсов или уроков в базе. Сначала создайте материалы.'))
            return

        # Способы оплаты
        payment_methods = ['cash', 'transfer']

        # Создаем 10 тестовых платежей
        for i in range(10):
            # Выбираем случайного пользователя
            user = random.choice(users)

            # Случайно выбираем: оплата курса или урока
            pay_for_course = random.choice([True, False])

            paid_course = None
            paid_lesson = None

            if pay_for_course and courses:
                paid_course = random.choice(courses)
                # Сумма для курса (например, от 1000 до 50000)
                amount = Decimal(random.randint(1000, 50000))
            elif lessons:
                paid_lesson = random.choice(lessons)
                # Сумма для урока (например, от 100 до 5000)
                amount = Decimal(random.randint(100, 5000))
            else:
                # Если нет уроков, но есть курсы
                paid_course = random.choice(courses)
                amount = Decimal(random.randint(1000, 50000))

            # Создаем платеж
            payment = Payment.objects.create(
                user=user,
                paid_course=paid_course,
                paid_lesson=paid_lesson,
                amount=amount,
                payment_method=random.choice(payment_methods)
            )

            self.stdout.write(
                self.style.SUCCESS(f'Создан платеж: {payment.user.email} - {payment.amount}₽')
            )

        self.stdout.write(
            self.style.SUCCESS('Успешно создано 10 тестовых платежей')
            )