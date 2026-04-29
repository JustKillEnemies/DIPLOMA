from src.core.config import Settings


def test_settings_host_for_dev_environment():
    settings = Settings(ENVIRONMENT="dev")
    assert settings.APP_HOST == "127.0.0.1"


def test_settings_host_for_prod_environment():
    settings = Settings(ENVIRONMENT="prod")
    assert settings.APP_HOST == "0.0.0.0"


def test_settings_default_values_are_present():
    settings = Settings()
    assert isinstance(settings.APP_PORT, int)
    assert settings.KAFKA_TOPIC_ORDERS == "production_orders"
