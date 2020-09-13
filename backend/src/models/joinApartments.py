from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


class JoinApartmentBase(BaseModel):
    user_id: int
    apartment_id: int

    class Config:
        orm_mode = True


class JoinApartmentUpdate(BaseModel):
    comments: Optional[str]
    activeStatus: str


class JoinApartmentResponse(JoinApartmentBase):
    joinApartment_id: int
    user_id: int
    apartment_id: int
    activeStatus: str
    comments: Optional[str]
    joined_on: Optional[datetime]

    class Config:
        orm_mode = True
