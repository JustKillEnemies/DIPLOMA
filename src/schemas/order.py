from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from uuid import UUID

class MESTask(BaseModel):
    # 1. Уникальный идентификатор
    order_id: UUID = Field(
        ..., 
        description="Уникальный идентификатор заказа (UUID v4)"
    )
    
    # 2. Артикул изделия
    item_code: str = Field(
        ..., 
        min_length=1, 
        description="Артикул или внутренний код готового изделия"
    )
    
    # 3. Материал (марка стали)
    steel_grade: str = Field(
        ..., 
        min_length=2, 
        max_length=20, 
        description="Марка стали (согласно ГОСТ или ТУ)"
    )
    
    # 4. Прослеживаемость (номер плавки)
    heat_number: str = Field(
        ..., 
        min_length=2, 
        max_length=30, 
        description="Номер плавки металла для обеспечения прослеживаемости"
    )
    
    # 5. Количественные характеристики
    quantity: int = Field(
        ..., 
        gt=0, 
        description="Количество изделий в принимаемой партии (должно быть > 0)"
    )
    
    # 6. Место возникновения события
    workshop_id: str = Field(
        ..., 
        min_length=2, 
        description="Идентификатор производственного цеха или участка"
    )
    
    # 7. Системное время
    sent_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Дата и время отправки сообщения в формате ISO 8601"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True, # Автоматическое удаление лишних пробелов в строках
        json_schema_extra={
            "example": {
                "order_id": "550e8400-e29b-41d4-a716-446655440000",
                "item_code": "VAL-001",
                "steel_grade": "45",
                "heat_number": "12345",
                "quantity": 10,
                "workshop_id": "WS-01",
            }
        }
    )