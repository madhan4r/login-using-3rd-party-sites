from sqlalchemy.orm import Session
from datetime import datetime

from ..models.apartments import ApartmentBase
from ..db_models.apartments import apartment_table
from fastapi.exceptions import HTTPException

def get_all(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(apartment_table).offset(skip).limit(limit).all()

def get_by_id(db_session: Session, apartment_id: int):
    apartment = db_session.query(apartment_table).filter(
        apartment_table.apartment_id == apartment_id).first()
    if not apartment:
        raise HTTPException(
            status_code=400, detail='Requested apartment ID ' + str(apartment_id) + ' does not exist')
    return apartment

def create_apartment(db_session: Session, apartment_data: ApartmentBase):
    apartment = apartment_table(**apartment_data.dict(exclude_unset=True))
    apartment_exists = db_session.query(apartment_table).filter(
        apartment_table.apartment_name == apartment.apartment_name).first()
    apartment.active = "for review"
    if apartment_exists:
        raise HTTPException(
            status_code=400, detail='Apartment Name already exists')
    apartment.created_on = datetime.now()
    return save(db_session, apartment)

def update_apartment(db_session: Session, apartment_id: int, apartment_data: ApartmentBase):
    apartment = get_by_id(db_session, apartment_id)
    apartment_update = apartment_data.dict(exclude_unset=True)
    for field in apartment_update:
        setattr(apartment, field, apartment_update[field])
    return save(db_session, apartment)


def save(db_session: Session, apartment: apartment_table):
    db_session.add(apartment)
    db_session.commit()
    db_session.refresh(apartment)
    return apartment