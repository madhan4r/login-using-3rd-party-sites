from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


class JoinApartmentBase(BaseModel):
    user_id: int
    apartment_id: int


class Config:
    orm_mode = True


class JoinApartmentResponse(JoinApartmentBase):
    joinApartment_id: int
    status: str
    user_id: int
    apartment_id: int
    joined_on: datetime

    class Config:
        orm_mode = True
