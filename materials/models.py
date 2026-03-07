from django.db import models
from users.models import User


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    preview = models.ImageField(
        upload_to='materials/previews/',
        verbose_name='Превью',
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    preview = models.ImageField(
        upload_to='materials/lessons/previews/',
        verbose_name='Превью',
        blank=True,
        null=True
    )
    video_link = models.URLField(
        verbose_name='Ссылка на видео',
        blank=True,
        null=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons',
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title