from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    name: str
    description: str | None
    cost: int


class EquipmentResponse(EquipmentCreate):
    id: int

    class Config:
        from_attributes = True
