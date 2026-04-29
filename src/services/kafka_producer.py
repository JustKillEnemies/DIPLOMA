import json
import logging
from kafka import KafkaProducer
import time

from src.core.config import settings
from src.schemas.order import MESTask

logger = logging.getLogger(__name__)

class OrderProducer:
    def __init__(self):
        self.producer = None
        self._initialize()

    def _initialize(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: str(k).encode('utf-8'),

                acks='all',              # Ждем подтверждения от всех копий
                retries=settings.KAFKA_RETRIES,               # Пять попыток переотправки при сбоях
                retry_backoff_ms=1000,   # Пауза в 1 сек между попытками
                request_timeout_ms=30000 # Ждем ответа от брокера 30 сек
            )
        except Exception as e:
            logger.error(f"Kafka error: {e}")

    def send_task(self, task: MESTask):
        if not self.producer: return False
        try:
            start_kafka = time.perf_counter() # Засекаем Кафку
            
            payload = task.model_dump(mode='json')
            self.producer.send(settings.KAFKA_TOPIC_ORDERS, key=task.order_id, value=payload)
            
            duration = time.perf_counter() - start_kafka
            logger.debug(f"Kafka Ingestion Time: {duration:.4f}s")
            return True
        except Exception:
            return False

kafka_service = OrderProducer()