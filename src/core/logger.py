import logging
import sys
from src.core.config import settings

def setup_logging():
    """
    Настройка системы логирования проекта.
    """
    # Формат: [Время] [Уровень] [Имя модуля]: Сообщение
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
    
    logging.basicConfig(
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout) # Вывод в консоль
        ]
    )

    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("kafka").setLevel(logging.WARNING)


logger = logging.getLogger("mes_gateway")