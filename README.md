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
- GitHub Actions

## Запуск через Docker Compose

### Требования
- Docker
- Docker Compose

### Шаги для запуска

1. **Клонируйте репозиторий**
   ```bash
   git clone <your-repo-url>
   cd DRF_Project
Создайте файл .env на основе шаблона

bash
cp .env.example .env
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

### Настройка удаленного сервера
Требования к серверу
Ubuntu 22.04/24.04

Python 3.13

PostgreSQL

Nginx

Git

Шаги настройки
Подключитесь к серверу по SSH

bash
ssh user@your-server-ip
Установите зависимости

bash
sudo apt update && sudo apt install -y python3-pip python3-venv nginx git postgresql supervisor
Клонируйте репозиторий

bash
git clone https://github.com/Akmal-coder/DRF_Project.git project
cd project
Настройте виртуальное окружение и установите зависимости

bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Настройте PostgreSQL

bash
sudo -u postgres psql
CREATE DATABASE drf_project;
CREATE USER test1 WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE drf_project TO test1;
\q
Создайте файл .env

bash
cp .env.example .env
# Отредактируйте настройки (DB_HOST=localhost, DEBUG=False и т.д.)
Выполните миграции и соберите статику

bash
python manage.py migrate
python manage.py collectstatic --noinput
Настройте Gunicorn как systemd-сервис (см. файл gunicorn.service в репозитории)

Настройте Nginx (см. конфигурацию drf_project в sites-available)

Автоматический деплой (GitHub Actions)
Как это работает
При каждом push в ветку develop (или создании pull request):

Автоматически запускаются тесты проекта

При успешном прохождении тестов код обновляется на сервере

Применяются миграции и собирается статика

Перезапускаются Gunicorn и Nginx

Необходимые секреты в GitHub
В репозитории → Settings → Secrets and variables → Actions добавьте:

Secret name	Значение
SERVER_HOST	IP-адрес вашего сервера
SERVER_USER	Имя пользователя на сервере
SSH_PRIVATE_KEY	Приватный SSH-ключ (содержимое файла ~/.ssh/id_rsa)
Запуск деплоя
Сделайте push в ветку develop:

bash
git push origin develop
Или создайте pull request в develop

Перейдите во вкладку Actions репозитория GitHub для просмотра статуса

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


