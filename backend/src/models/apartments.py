from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


class ApartmentBase(BaseModel):
    apartment_name: str


class Config:
    orm_mode = True


class ApartmentResponse(ApartmentBase):
    apartment_id: int
    active: str
    created_on: datetime

    class Config:
        orm_mode = True
