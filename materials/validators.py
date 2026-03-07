import re
from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:
    """Валидатор для проверки, что ссылка ведет на youtube.com"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Получаем значение поля для валидации
        if isinstance(value, dict):
            field_value = value.get(self.field)
        else:
            field_value = value


        if not field_value:
            return


        if not re.search(r'(youtube\.com|youtu\.be)', field_value):
            raise ValidationError(
                f'Ссылка должна быть на youtube.com. Текущая ссылка: {field_value}'
            )


def validate_youtube_link(value):
    """Функция-валидатор для проверки ссылок на youtube"""
    if value and not re.search(r'(youtube\.com|youtu\.be)', value):
        raise ValidationError(
            f'Ссылка должна быть на youtube.com. Текущая ссылка: {value}'
        )
    return value