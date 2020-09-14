from sqlalchemy import Column, Integer, String, Table, DateTime, Date, text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class JoinApartments(Base):
    __tablename__ = "joinApartment_table"
    joinApartment_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey('user_table.user_id'), nullable=False)
    apartment_id = Column(ForeignKey(
        'apartment_table.apartment_id'), nullable=False)
    user_name = Column(String(255), nullable=False)
    activeStatus = Column(String(20), nullable=False)
    comments = Column(String(255), nullable=True)
    reviewed_on = Column(DateTime(timezone=True),
                         onupdate=func.now(), nullable=True)

    apartment_table = relationship("Apartments", back_populates="joinedUsers")
    user_table = relationship("Users", back_populates="joinedApartments")
