from sqlalchemy.orm import Session
from datetime import datetime

from ..models.apartments import ApartmentBase, ApartmentUpdate
from ..db_models.apartments import Apartments
from fastapi.exceptions import HTTPException
from ..db_models.joinApartments import JoinApartments


def get_all(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(Apartments).offset(skip).limit(limit).all()


def get_by_id(db_session: Session, apartment_id: int):
    apartment = db_session.query(Apartments).filter(
        Apartments.apartment_id == apartment_id).first()
    if not apartment:
        raise HTTPException(
            status_code=400, detail='Requested apartment ID ' + str(apartment_id) + ' does not exist')
    return apartment


def create_apartment(db_session: Session, apartment_data: ApartmentBase):
    apartment = Apartments(**apartment_data.dict(exclude_unset=True))
    apartment_exists = db_session.query(Apartments).filter(
        Apartments.apartment_name == apartment.apartment_name).first()
    apartment.activeStatus = "under review"
    if apartment_exists:
        raise HTTPException(
            status_code=400, detail='Apartment Name already exists')
    apartment.created_on = datetime.now()
    apartment = save(db_session, apartment)
    if apartment:
        joinApartment_data = JoinApartments(
            user_id=apartment.created_by, apartment_id=apartment.apartment_id, activeStatus="Joined")
        save(db_session, joinApartment_data)
    return apartment


def update_apartment(db_session: Session, apartment_id: int, apartment_data: ApartmentUpdate):
    apartment = get_by_id(db_session, apartment_id)
    apartment_update = apartment_data.dict(exclude_unset=True)
    for field in apartment_update:
        setattr(apartment, field, apartment_update[field])
    apartment.activated_on = datetime.now()
    return save(db_session, apartment)


def save(db_session: Session, apartment: Apartments):
    db_session.add(apartment)
    db_session.commit()
    db_session.refresh(apartment)
    return apartment
