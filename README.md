# DRF Project

## Технологии

- Python 3.13
- Django
- Django REST Framework
- Poetry
- SQLite


## API Endpoints
Курсы (ViewSet)
GET /api/courses/ - список курсов

POST /api/courses/ - создать курс

GET /api/courses/{id}/ - получить курс

PUT/PATCH /api/courses/{id}/ - обновить курс

DELETE /api/courses/{id}/ - удалить курс

Уроки (Generic views)
GET /api/lessons/ - список уроков

POST /api/lessons/ - создать урок

GET /api/lessons/{id}/ - получить урок

PUT/PATCH /api/lessons/{id}/ - обновить урок

DELETE /api/lessons/{id}/ - удалить урок

## Модели
User (кастомная)
Email (авторизация)

Телефон

Город

Аватар

Course
Название

Превью

Описание

Lesson
Название

Описание

Превью

Ссылка на видео

Связь с курсом (ForeignKey)


