from pydantic import BaseModel

class EquipmentCreate(BaseModel):
    name: str
    description: str | None
    cost: int

class EquipmentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    cost: int

    class Config:
        from_attributes = True