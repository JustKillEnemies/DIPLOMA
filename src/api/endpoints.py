import secrets
from fastapi import APIRouter, Header, Depends, HTTPException, status
from fastapi.security import APIKeyHeader # Специальный класс для OpenAPI

from src.schemas.order import MESTask
from src.services.kafka_producer import kafka_service
from src.core.config import settings
from src.core.logger import logger

router = APIRouter()

# 1. Определяем схему безопасности для OpenAPI (Swagger)
# name="X-API-Key" — это название заголовка, который будет искать система
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    """
    Проверка API-ключа с защитой от тайминг-атак.
    """
    if not api_key_header:
        logger.warning("[SECURITY] Запрос без API-ключа")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing"
        )
    
    # 2. secrets.compare_digest сравнивает строки за фиксированное время.
    # Это защищает от подбора ключа путем замера скорости ответа сервера.
    if not secrets.compare_digest(api_key_header, settings.API_KEY_SECRET):
        logger.warning(f"[SECURITY] Неверный API-ключ: {api_key_header[:4]}***")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    
    return api_key_header

@router.post(
    "/tasks", 
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_api_key)] # Защищаем весь эндпоинт
)
async def receive_task(task: MESTask):
    """
    Прием задания от MES. Доступ разрешен только при наличии валидного X-API-Key.
    """
    logger.info(f"[INGRESS] Принято задание {task.order_id}")

    if not kafka_service.send_task(task):
        logger.error(f"[SYSTEM] Ошибка Kafka для заказа {task.order_id}")
        raise HTTPException(status_code=500, detail="Internal Broker Error")
        
    return {"status": "accepted", "id": task.order_id}