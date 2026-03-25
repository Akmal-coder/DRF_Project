# DRF Project

## Технологии

- Python 3.13
- Django
- Django REST Framework
- Poetry
- PostgreSQL
- Redis
- Celery
- Docker

## Запуск через Docker Compose

### Требования
- Docker
- Docker Compose

### Шаги для запуска

1. **Клонируйте репозиторий**
   ```bash
   git clone <your-repo-url>
   cd DRF_Project
Создайте файл .env на основе шаблона bash cp .env.example .env
(при необходимости отредактируйте настройки)

Соберите и запустите контейнеры

bash
docker-compose up -d --build
Примените миграции

bash
docker-compose exec backend python manage.py migrate
Создайте суперпользователя (опционально)

bash
docker-compose exec backend python manage.py createsuperuser
Проверка работоспособности
Сервис	Команда проверки
Backend	Откройте http://localhost:8000
PostgreSQL	docker-compose exec db pg_isready -U postgres
Redis	docker-compose exec redis redis-cli ping (должен вернуть PONG)
Celery Worker	docker-compose logs celery
Celery Beat	docker-compose logs celery-beat
Остановка проекта
bash
docker-compose down
Остановка с удалением данных
bash
docker-compose down -v
API Endpoints
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

Аутентификация
POST /api/token/ - получение JWT токена

POST /api/token/refresh/ - обновление токена

POST /api/register/ - регистрация пользователя

Подписки
POST /api/subscription/ - подписаться/отписаться от курса

Платежи (Stripe)
GET /api/payments/ - список платежей

POST /api/payments/create/ - создать платеж

Модели
User (кастомная)
Email (авторизация)

Телефон

Город

Аватар

Course
Название

Превью

Описание

Владелец

Цена

Lesson
Название

Описание

Превью

Ссылка на видео

Связь с курсом (ForeignKey)

Владелец

Payment
Пользователь

Дата оплаты

Оплаченный курс/урок

Сумма

Способ оплаты

Stripe поля

Subscription
Пользователь

Курс

Дата подписки


