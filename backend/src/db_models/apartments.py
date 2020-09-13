from sqlalchemy import Column, Integer, String, Table, DateTime, Date, text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Apartments(Base):
    __tablename__ = "apartment_table"
    apartment_id = Column(Integer, primary_key=True, nullable=False)
    apartment_name = Column(String(255), unique=True, nullable=False)
    active = Column(Boolean, nullable=False)
    created_by = Column(ForeignKey('user_table.user_id'), nullable=False)
    created_on = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    joinedUsers = relationship(
        "JoinApartments", back_populates="apartment_table")      
    owner = relationship("Users", back_populates="createdApartments")
