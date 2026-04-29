import pytest
from pydantic import ValidationError

from src.schemas.order import MESTask


def test_mes_task_valid_payload(valid_task_payload):
    task = MESTask(**valid_task_payload)
    assert task.order_id == "ORD-001"
    assert task.target_temp_c == 1200


def test_mes_task_rejects_invalid_op_number(valid_task_payload):
    valid_task_payload["op_number"] = "OP-10"

    with pytest.raises(ValidationError):
        MESTask(**valid_task_payload)


def test_mes_task_rejects_soaking_greater_than_heating(valid_task_payload):
    valid_task_payload["soaking_time_min"] = 200

    with pytest.raises(ValidationError):
        MESTask(**valid_task_payload)


def test_mes_task_rejects_finish_temp_not_lower_than_target(valid_task_payload):
    valid_task_payload["min_finish_temp_c"] = valid_task_payload["target_temp_c"]

    with pytest.raises(ValidationError):
        MESTask(**valid_task_payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("ingot_weight", 0),
        ("c_content", 6.0),
        ("target_temp_c", 2000),
        ("target_length_mm", -1),
    ],
)
def test_mes_task_rejects_out_of_range_values(valid_task_payload, field, value):
    valid_task_payload[field] = value

    with pytest.raises(ValidationError):
        MESTask(**valid_task_payload)
