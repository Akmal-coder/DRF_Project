FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.0.0


COPY pyproject.toml poetry.lock* /app/


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root


COPY . /app/


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]