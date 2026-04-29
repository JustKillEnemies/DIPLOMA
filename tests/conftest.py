import copy
import os

import pytest


# Make tests deterministic even if local .env has non-boolean DEBUG values.
os.environ["DEBUG"] = "false"
os.environ.setdefault("ENVIRONMENT", "dev")
os.environ.setdefault("API_KEY_SECRET", "test-secret")


@pytest.fixture
def valid_task_payload() -> dict:
    payload = {
        "order_id": "ORD-001",
        "work_center": "PRESS-01",
        "op_number": "OP10",
        "timestamp": "2026-01-01T12:00:00",
        "heat_id": "12345",
        "steel_grade": "45",
        "ingot_weight": 1200.5,
        "ingot_type": "round",
        "c_content": 0.45,
        "si_content": 0.25,
        "mn_content": 0.8,
        "s_content": 0.02,
        "p_content": 0.015,
        "furnace_id": "F-01",
        "target_temp_c": 1200,
        "heating_duration_min": 180,
        "soaking_time_min": 60,
        "press_force_mn": 45.0,
        "reduction_ratio_target": 2.5,
        "die_id": "DIE-01",
        "min_finish_temp_c": 900,
        "target_shape": "shaft",
        "target_length_mm": 1500,
        "target_diameter_mm": 300,
    }
    return copy.deepcopy(payload)
