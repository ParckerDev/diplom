from pydantic import BaseModel

class EquipmentBase(BaseModel):
    name: str
    discription: str

class EquipmentCreate(EquipmentBase):
    pass

class Equipment(EquipmentBase):
    id: int


    class Config:
        from_attributes=True