from pydantic import BaseModel
from datetime import datetime


class RentalCreate(BaseModel):
    equipment_id: int
    user_id: int
    start_date: datetime
    end_date: datetime


class RentalResponse(RentalCreate):
    id: int

    class Config:
        from_attributes = True
