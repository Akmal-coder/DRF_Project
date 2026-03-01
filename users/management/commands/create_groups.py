from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from materials.models import Course, Lesson


class Command(BaseCommand):
    """Кастомная команда для создания групп"""
    help = 'Создает группы модераторов и назначает права'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderators_group, created = Group.objects.get_or_create(name='Модераторы')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модераторы" уже существует'))

        # Получаем permissions для курсов и уроков (просмотр и редактирование)
        content_types = [
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Lesson),
        ]

        # Права на просмотр и изменение (но не создание и удаление)
        permissions = Permission.objects.filter(
            content_type__in=content_types,
            codename__in=['view_course', 'change_course', 'view_lesson', 'change_lesson']
        )

        # Назначаем права группе
        moderators_group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(f'Назначено {permissions.count()} прав группе "Модераторы"')
        )