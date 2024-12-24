from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    telephone_number: str


class UserCreate(UserBase):
    pass


class User_id(UserBase):
    id: int

    class Config:
        orm_mode = True
