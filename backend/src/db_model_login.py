from sqlalchemy import Column, Integer, String, Table, DateTime, text
# from datetime import date
from .database import Base


class user_table(Base):
    __tablename__ = "user_table"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    # dob = Column(date, nullable=False)
    gender = Column(String(11), nullable=False)
    email = Column(String(255), nullable=False)
    phone_no = Column(String(13), nullable=True)
    created_by = Column(String(20), nullable=False)
    # created_on = Column(DateTime, server_default=text("now()"), nullable=False)
    # modified_on = Column(DateTime, nullable=True)
