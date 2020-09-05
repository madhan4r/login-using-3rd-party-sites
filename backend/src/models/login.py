from typing import Optional
from pydantic import BaseModel


class formData(BaseModel):
    email: str
    password: str

class loginTypeData(BaseModel):
    email: Optional[str]
    user_name: Optional[str]
    google_id: Optional[str]
    facebook_id: Optional[str]
