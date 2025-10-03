"""
Конфигурация приложения с использованием pydantic-settings
"""
import secrets

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """Настройки базы данных"""
    name: str = Field(default="hotel_booking", description="Название базы данных")
    user: str = Field(default="postgres", description="Пользователь БД")
    password: str = Field(default="postgres", description="Пароль БД")
    host: str = Field(default="localhost", description="Хост БД")
    port: int = Field(default=5433, description="Порт БД")


class DjangoSettings(BaseModel):
    """Настройки Django"""
    debug: bool = Field(default=True, description="Режим отладки")
    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Секретный ключ"
    )
    allowed_hosts: list[str] = Field(default=["*"], description="Разрешенные хосты")


class APISettings(BaseModel):
    """Настройки API"""
    max_page_size: int = Field(default=100, description="Максимальный размер страницы")
    default_page_size: int = Field(default=20, description="Размер страницы по умолчанию")


class LoggingSettings(BaseModel):
    """Настройки логирования"""
    level: str = Field(default="INFO", description="Уровень логирования")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Формат логов"
    )


class Settings(BaseSettings):
    """Основные настройки приложения"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore"
    )

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    django: DjangoSettings = Field(default_factory=DjangoSettings)
    api: APISettings = Field(default_factory=APISettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    # Переменные окружения для обратной совместимости
    debug: bool = Field(default=True, alias="DJANGO_DEBUG")
    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        alias="DJANGO_SECRET_KEY"
    )
    database_url: str | None = Field(default=None, alias="DATABASE_URL")


# Глобальный экземпляр настроек
settings = Settings()


def get_database_config() -> dict:
    """Получить конфигурацию базы данных для Django"""
    if settings.database_url:
        # Если указан DATABASE_URL, используем его
        return {"ENGINE": "django.db.backends.postgresql"}

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.database.name,
        "USER": settings.database.user,
        "PASSWORD": settings.database.password,
        "HOST": settings.database.host,
        "PORT": settings.database.port,
    }


def get_django_settings() -> dict:
    """Получить настройки Django"""
    return {
        "DEBUG": settings.django.debug,
        "SECRET_KEY": settings.django.secret_key,
        "ALLOWED_HOSTS": settings.django.allowed_hosts,
    }
