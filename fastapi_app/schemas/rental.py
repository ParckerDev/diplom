from datetime import datetime
from pydantic import BaseModel


class RentalBase(BaseModel):
    equipment_id: int
    user_id: int
    start_date: datetime
    end_date: datetime


class RentalCreate(RentalBase):
    pass


class Rental_id(RentalBase):
    id: int

    class Config:
        orm_model = True
