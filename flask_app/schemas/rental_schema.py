from pydantic import BaseModel
from datetime import datetime

class RentalCreate(BaseModel):
    user_id: int
    start_date: datetime
    end_date: datetime

class RentalResponse(BaseModel):
    id: int
    equipment_id: int
    user_id: int
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True
