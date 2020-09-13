from sqlalchemy.orm import Session
from datetime import datetime

from ..models.joinApartments import JoinApartmentBase, JoinApartmentUpdate
from ..db_models.joinApartments import JoinApartments
from fastapi.exceptions import HTTPException


def get_all(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(JoinApartments).offset(skip).limit(limit).all()


def get_by_id(db_session: Session, joinApartment_id: int):
    joinApartment = db_session.query(JoinApartments).filter(
        JoinApartments.joinApartment_id == joinApartment_id).first()
    if not joinApartment:
        raise HTTPException(
            status_code=400, detail='Requested joinApartment ID ' + str(joinApartment_id) + ' does not exist')
    return joinApartment


def join_apartment(db_session: Session, joinApartment_data: JoinApartmentBase):
    joinApartment = JoinApartments(
        **joinApartment_data.dict(exclude_unset=True))
    joinApartment_exists = db_session.query(JoinApartments).filter(
        JoinApartments.apartment_id == joinApartment.apartment_id,
        JoinApartments.user_id == joinApartment_data.user_id).first()
    joinApartment.status = False
    if joinApartment_exists:
        raise HTTPException(
            status_code=400, detail='You have already joined this Apartment')
    joinApartment.created_on = datetime.now()
    return save(db_session, joinApartment)


def update_join_apartment(db_session: Session, joinApartment_id: int, joinApartment_data: JoinApartmentUpdate):
    joinApartment = get_by_id(db_session, joinApartment_id)
    joinApartment_update = joinApartment_data.dict(exclude_unset=True)
    for field in joinApartment_update:
        setattr(joinApartment, field, joinApartment_update[field])
    joinApartment.joined_on = datetime.now()
    return save(db_session, joinApartment)


def save(db_session: Session, joinApartment: JoinApartments):
    db_session.add(joinApartment)
    db_session.commit()
    db_session.refresh(joinApartment)
    return joinApartment
