from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """Класс для конфигурации настроек бд"""

    APP_DB_USER: str = 'postgres'
    APP_DB_PASS: str = ''
    APP_DB_HOST: str = 'localhost'
    APP_DB_PORT: int = 5432
    APP_DB_NAME: str = 'registration_service_dev'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

database_config = DatabaseConfig()
