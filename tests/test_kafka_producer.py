from unittest.mock import Mock

from src.schemas.order import MESTask
from src.services import kafka_producer as kafka_module


def test_order_producer_initialize_success(monkeypatch):
    fake_producer = object()
    monkeypatch.setattr(kafka_module, "KafkaProducer", lambda **kwargs: fake_producer)

    producer = kafka_module.OrderProducer()

    assert producer.producer is fake_producer


def test_order_producer_initialize_failure(monkeypatch):
    def raise_error(**kwargs):
        raise RuntimeError("kafka unavailable")

    monkeypatch.setattr(kafka_module, "KafkaProducer", raise_error)

    producer = kafka_module.OrderProducer()

    assert producer.producer is None


def test_send_task_returns_false_without_producer(valid_task_payload):
    producer = kafka_module.OrderProducer.__new__(kafka_module.OrderProducer)
    producer.producer = None
    task = MESTask(**valid_task_payload)

    assert producer.send_task(task) is False


def test_send_task_sends_payload_and_returns_true(valid_task_payload):
    producer = kafka_module.OrderProducer.__new__(kafka_module.OrderProducer)
    producer.producer = Mock()
    task = MESTask(**valid_task_payload)

    result = producer.send_task(task)

    assert result is True
    producer.producer.send.assert_called_once()
    args, kwargs = producer.producer.send.call_args
    assert args[0] == kafka_module.settings.KAFKA_TOPIC_ORDERS
    assert kwargs["key"] == task.order_id
    assert kwargs["value"] == task.model_dump(mode="json")


def test_send_task_returns_false_when_send_raises(valid_task_payload):
    producer = kafka_module.OrderProducer.__new__(kafka_module.OrderProducer)
    producer.producer = Mock()
    producer.producer.send.side_effect = RuntimeError("send failed")
    task = MESTask(**valid_task_payload)

    assert producer.send_task(task) is False
