from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel
from .joinApartments import JoinApartmentResponse


class ApartmentBase(BaseModel):
    apartment_name: str
    created_by: int


class Config:
    orm_mode = True


class ApartmentUpdate(BaseModel):
    comments: Optional[str]
    activeStatus: str


class ApartmentResponse(ApartmentBase):
    apartment_id: int
    activeStatus: str
    created_by: int
    created_on: datetime
    comments: Optional[str]
    activated_on: Optional[datetime]
    joinedUsers: List[JoinApartmentResponse] = []

    class Config:
        orm_mode = True
