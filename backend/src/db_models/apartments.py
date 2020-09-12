from sqlalchemy import Column, Integer, String, Table, DateTime, Date, text, ForeignKey
from sqlalchemy.sql import func
from ..database import Base
from .user import user_table


class apartment_table(Base):
    __tablename__ = "apartment_table"
    apartment_id = Column(Integer, primary_key=True, nullable=False)
    apartment_name = Column(String(255), unique=True, nullable=False)
    active = Column(String, nullable=False)
    created_by = Column(Integer,ForeignKey('user_table.user_id'))
    created_on = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    # user = relationship("user_table", secondary=Link,
    #                     back_populates="apartment")
