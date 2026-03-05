import os
from typing import Literal
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. Окружение: может быть либо 'dev', либо 'prod'
    # По умолчанию 'dev', если не задано в .env
    ENVIRONMENT: Literal["dev", "prod"] = os.getenv("ENVIRONMENT", "dev")

    # 2. Метаданные проекта
    PROJECT_NAME: str = "Передача заказов от MES"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # 3. Параметры запуска сервера
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))

    @computed_field
    @property
    def APP_HOST(self) -> str:
        """
        Динамический выбор хоста: 
        В продакшене  — 0.0.0.0
        В разработке  — 127.0.0.1
        """
        return "0.0.0.0" if self.ENVIRONMENT == "prod" else "127.0.0.1"

    # 4. Настройки Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC_ORDERS: str = "production_orders"
    KAFKA_CLIENT_ID: str = "mes_ingress_gateway"
    KAFKA_RETRIES: int = 5 

    # 5. Безопасность
    API_KEY_SECRET: str = os.getenv("API_KEY_SECRET", "default-dev-secret-key")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()