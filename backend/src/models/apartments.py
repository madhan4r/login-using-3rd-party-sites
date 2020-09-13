from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel
from .joinApartments import JoinApartmentResponse


class ApartmentBase(BaseModel):
    apartment_name: str
    created_by: int


class Config:
    orm_mode = True


class ApartmentResponse(ApartmentBase):
    apartment_id: int
    active: str
    created_by: int
    created_on: datetime
    joinedUsers: List[JoinApartmentResponse] = []
    
    class Config:
        orm_mode = True
