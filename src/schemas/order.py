from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from datetime import datetime
import re


class MESTask(BaseModel):
    # --- 1. Метаданные ---
    order_id: str = Field(..., min_length=1)
    work_center: str = Field(..., min_length=1)
    op_number: str = Field(..., min_length=1)
    timestamp: datetime

    # --- 2. Заготовка ---
    heat_id: str = Field(..., min_length=1)
    steel_grade: str = Field(..., min_length=1)
    ingot_weight: float = Field(..., gt=0)
    ingot_type: str = Field(..., min_length=1)

    # --- 3. Химия ---
    c_content: float = Field(..., ge=0.0, le=5.0)
    si_content: float = Field(..., ge=0.0, le=3.0)
    mn_content: float = Field(..., ge=0.0, le=5.0)
    s_content: float = Field(..., ge=0.0, le=0.5)
    p_content: float = Field(..., ge=0.0, le=0.5)

    # --- 4. Нагрев ---
    furnace_id: str = Field(..., min_length=1)
    target_temp_c: int = Field(..., ge=20, le=1500)
    heating_duration_min: int = Field(..., gt=0)
    soaking_time_min: int = Field(..., gt=0)

    # --- 5. Обработка ---
    press_force_mn: float = Field(..., gt=0)
    reduction_ratio_target: float = Field(..., ge=1.0)
    die_id: str = Field(..., min_length=1)
    min_finish_temp_c: int

    # --- 6. Геометрия ---
    target_shape: str = Field(..., min_length=1)
    target_length_mm: float = Field(..., gt=0)
    target_diameter_mm: float = Field(..., gt=0)

    # --- ВАЛИДАТОРЫ ---

    @field_validator("op_number")
    @classmethod
    def validate_op_number(cls, v):
        if not re.match(r"^[a-zA-Z0-9]+$", v):
            raise ValueError("op_number должен содержать только буквы и цифры")
        return v

    @model_validator(mode="after")
    def validate_logic(self):
        # soaking <= heating
        if self.soaking_time_min > self.heating_duration_min:
            raise ValueError("soaking_time_min не может быть больше heating_duration_min")

        # finish temp < heating temp
        if self.min_finish_temp_c >= self.target_temp_c:
            raise ValueError("min_finish_temp_c должен быть меньше target_temp_c")

        return self

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
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
                "target_diameter_mm": 300
            }
        }
    )