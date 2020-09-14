from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


class JoinApartmentBase(BaseModel):
    user_id: int
    apartment_id: int
    user_name: str

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
    reviewed_on: Optional[date]
    comments: Optional[str]

    class Config:
        orm_mode = True
