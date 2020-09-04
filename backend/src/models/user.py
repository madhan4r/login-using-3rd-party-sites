from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel

# User Base Class


class UserBase(BaseModel):
    user_name: Optional[str]
    dob: Optional[date]
    gender: Optional[str]
    email: Optional[str]
    phone_no: Optional[str]
    login_type: Optional[str]
    facebook_id: Optional[str]


class UserCreate(UserBase):
    user_name: str
    dob: date
    gender: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    user_id: int
    created_on: datetime
    modified_on: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: Optional[str]
    password: Optional[str]
    user_data: Optional[str] 