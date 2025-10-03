FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Установка poetry
RUN pip install poetry

# Копирование файлов с зависимостями
COPY pyproject.toml poetry.lock* /code/

# Настройка poetry для установки в системный Python
RUN poetry config virtualenvs.create false

# Установка зависимостей без установки текущего проекта
RUN poetry install --no-interaction --no-ansi --no-root

# Копирование только кода приложения
COPY src /code/

