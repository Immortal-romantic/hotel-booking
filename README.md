# 🏨 Hotel Booking API

Простой сервис для управления номерами отелей и бронированиями на базе Django REST Framework.

## ✨ Возможности

- **Управление номерами отеля**: создание, удаление, просмотр с сортировкой
- **Система бронирования**: создание броней с проверкой дат и отсутствием пересечений
- **Валидация данных**: проверка корректности дат и предотвращение конфликтов
- **RESTful API**: современное HTTP JSON API
- **Тестирование**: полное покрытие юнит-тестами (11 тестов)
- **Docker поддержка**: готовность к развертыванию в контейнерах
- **Современные инструменты разработки**: Poetry, Ruff, Pre-commit, CI/CD
- **Конфигурация**: гибкая настройка через YAML с pydantic-settings
- **Безопасность**: проверка зависимостей и секретов

## 🚀 Быстрый запуск

### Локальный запуск

1. **Установите зависимости:**
```bash
pip install -r requirements.txt
# или
poetry install
```

2. **Настройте базу данных:**
```bash
python src/manage.py migrate
```

3. **Запустите сервер:**
```bash
python src/manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000`

### Запуск с Docker

```bash
docker-compose up --build
```

## 📚 API Документация

### Номера отеля

#### Создать номер
```http
POST /rooms/create
Content-Type: application/json

{
  "description": "Люкс с видом на море",
  "price": 150.00
}
```

**Ответ:**
```json
{
  "room_id": 1
}
```

#### Удалить номер
```http
POST /rooms/delete
Content-Type: application/json

{
  "room_id": 1
}
```

**Ответ:**
```json
{
  "ok": true
}
```

#### Получить список номеров
```http
GET /rooms/list?sort_by=price&order=asc
```

**Параметры запроса:**
- `sort_by`: `price` или `created_at` (по умолчанию: `id`)
- `order`: `asc` или `desc` (по умолчанию: `asc`)

**Ответ:**
```json
[
  {
    "room_id": 1,
    "description": "Люкс с видом на море",
    "price": "150.00",
    "created_at": "2023-12-01T10:30:00Z"
  }
]
```

### Бронирования

#### Создать бронь
```http
POST /bookings/create
Content-Type: application/json

{
  "room_id": 1,
  "date_start": "2023-12-25",
  "date_end": "2023-12-27"
}
```

**Ответ:**
```json
{
  "booking_id": 1
}
```

#### Удалить бронь
```http
POST /bookings/delete
Content-Type: application/json

{
  "booking_id": 1
}
```

**Ответ:**
```json
{
  "ok": true
}
```

#### Получить список броней номера
```http
GET /bookings/list?room_id=1
```

**Ответ:**
```json
[
  {
    "booking_id": 1,
    "date_start": "2023-12-25",
    "date_end": "2023-12-27"
  }
]
```

## 🛠️ Разработка

### Тестирование

```bash
# Запуск всех тестов
pytest -v

# Запуск конкретного файла
pytest src/tests/test.py -v

# Запуск с покрытием
pytest --cov=src

# Запуск с отчетом о покрытии в HTML
pytest --cov=src --cov-report=html
```

### Линтинг и форматирование

```bash
# Проверка кода
ruff check .

# Автоматическое исправление
ruff check . --fix

# Форматирование кода
ruff format .

# Проверка только измененных файлов
ruff check --diff
```

### Pre-commit хуки

Проект использует pre-commit для автоматической проверки кода перед коммитом:

```bash
# Установка хуков
pre-commit install

# Запуск всех хуков вручную
pre-commit run --all-files

# Обновление хуков
pre-commit autoupdate
```

### Безопасность

```bash
# Проверка уязвимостей в зависимостях
safety check

# Статический анализ безопасности
bandit -r src/

# Проверка на наличие секретов
detect-secrets scan
```

### CI/CD

Проект включает настроенный GitHub Actions workflow для:

- ✅ Автоматического тестирования на Python 3.11
- ✅ Проверки кода линтерами (Ruff)
- ✅ Сборки Docker образов
- ✅ Анализа безопасности (Safety, Bandit)
- ✅ Отчета о покрытии тестами (Codecov)

### Структура проекта

```
hotel-booking/
├── src/                          # Исходный код Django
│   ├── api/                      # Приложение API
│   │   ├── models.py            # Модели Room и Booking
│   │   ├── serializers.py       # Сериализаторы
│   │   ├── views.py             # API представления
│   │   ├── urls.py              # URL маршруты
│   │   └── tests.py             # Тесты API
│   ├── hotel_booking/           # Основное приложение Django
│   │   ├── settings.py          # Настройки
│   │   ├── urls.py              # Главные URL
│   │   └── views.py             # Базовые представления
│   ├── tests/                   # Дополнительные тесты
│   │   └── test.py              # Основные тесты
│   └── manage.py                # Django management script
├── docker/                      # Docker файлы
│   ├── api/Dockerfile           # Dockerfile для API
│   └── db/init.sql              # Инициализация БД
├── docker-compose.yml           # Docker Compose конфигурация
├── pyproject.toml               # Зависимости и настройки
├── Makefile                     # Сборка проекта
└── README.md                    # Документация
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DJANGO_DEBUG` | Режим отладки | `True` |
| `DJANGO_SECRET_KEY` | Секретный ключ Django | `django-insecure-dev-key` |
| `USE_POSTGRESQL` | Использовать PostgreSQL вместо SQLite | `False` |
| `DATABASE_*` | Настройки подключения к PostgreSQL | - |

### Настройка PostgreSQL

Для использования PostgreSQL установите переменные окружения:

```bash
export USE_POSTGRESQL=true
export DATABASE_NAME=hotel_booking
export DATABASE_USER=your_user
export DATABASE_PASSWORD=your_password
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
```

## 🧪 Примеры использования

### cURL примеры

```bash
# Создать номер отеля
curl -X POST http://localhost:8000/rooms/create \
  -H "Content-Type: application/json" \
  -d '{"description": "Стандартный номер", "price": 100.00}'

# Создать бронь
curl -X POST http://localhost:8000/bookings/create \
  -H "Content-Type: application/json" \
  -d '{"room_id": 1, "date_start": "2023-12-25", "date_end": "2023-12-27"}'

# Получить список номеров
curl -X GET "http://localhost:8000/rooms/list?sort_by=price&order=asc"

# Получить брони номера
curl -X GET "http://localhost:8000/bookings/list?room_id=1"
```

### Python примеры

```python
import requests

base_url = "http://localhost:8000"

# Создать номер
response = requests.post(f"{base_url}/rooms/create", json={
    "description": "Президентский люкс",
    "price": 500.00
})
room_id = response.json()["room_id"]

# Создать бронь
response = requests.post(f"{base_url}/bookings/create", json={
    "room_id": room_id,
    "date_start": "2023-12-25",
    "date_end": "2023-12-27"
})
booking_id = response.json()["booking_id"]

print(f"Номер {room_id} забронирован под номером {booking_id}")
```

## ✅ Валидация и ограничения

### Правила валидации:
- **Даты**: `date_start` должна быть раньше `date_end`
- **Цены**: должны быть неотрицательными
- **Описание**: не может быть пустым
- **Пересечения**: номера не могут быть забронированы на пересекающиеся даты

### Обработка ошибок:
```json
{
  "error": "room is already booked on given dates"
}
```

## 🏗️ Архитектура

### Модели данных

**Room (Номер отеля):**
- `id`: Уникальный идентификатор
- `description`: Текстовое описание номера
- `price`: Цена за ночь (Decimal)
- `created_at`: Дата создания

**Booking (Бронирование):**
- `id`: Уникальный идентификатор брони
- `room`: Ссылка на номер отеля
- `date_start`: Дата начала бронирования
- `date_end`: Дата окончания бронирования
- `created_at`: Дата создания записи

### Индексы БД
- Индекс на `(room, date_start, date_end)` для быстрого поиска пересечений

## 🚀 Развертывание

### Сборка для продакшена

```bash
# Сборка статических файлов
python src/manage.py collectstatic

# Создание миграций (если нужно)
python src/manage.py makemigrations

# Применение миграций
python src/manage.py migrate
```

### Docker продакшн

```bash
# Сборка образов
docker-compose -f docker-compose.prod.yml build

# Запуск
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 Тестирование

Проект включает **11 юнит-тестов** с полным покрытием функционала:

- ✅ Создание и удаление номеров
- ✅ Создание и удаление броней
- ✅ Валидация дат и цен
- ✅ Проверка пересекающихся бронирований
- ✅ Сортировка и фильтрация
- ✅ Обработка ошибок

## 📈 Производительность

- **Оптимизированные запросы** с использованием Django ORM
- **Индексы** для быстрого поиска пересечений дат
- **Валидация на уровне БД** и приложения
- **RESTful API** с правильными HTTP статусами

## 🤝 Вклад в проект

1. Сделайте форк репозитория
2. Создайте ветку для новой функциональности
3. Добавьте тесты для нового функционала
4. Убедитесь, что все тесты проходят
5. Создайте Pull Request

## 📄 Лицензия

Этот проект является открытым исходным кодом.

## 🆘 Поддержка

При возникновении вопросов или проблем:
1. Проверьте раздел Issues в репозитории
2. Создайте новый Issue с подробным описанием проблемы
3. Укажите версию Python, Django и шаги для воспроизведения ошибки

---
