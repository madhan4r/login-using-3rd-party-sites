from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel

# User Base Class


class UserBase(BaseModel):
    user_id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    # dob: Optional[date]
    gender: Optional[str]
    email: Optional[str]
    phone_no: Optional[str]


class UserCreate(UserBase):
    first_name: str
    # dob: date
    email: str
    created_by: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    user_id: int

    class Config:
        orm_mode = True
