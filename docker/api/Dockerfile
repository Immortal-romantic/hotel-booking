FROM python:3.10-slim

WORKDIR /app

# Установка poetry
RUN pip install poetry==1.6.1

# Копирование файлов проекта
COPY pyproject.toml poetry.lock* /app/

# Настройка poetry для создания virtualenv в проекте
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копирование исходного кода
COPY src /app/src
COPY config.yaml /app/

# Команда запуска
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
