from sqlalchemy.orm import Session
import hashlib
import jwt
from datetime import datetime

from ..crud import user as user_crud
from ..models.login import formData, loginTypeData
from ..db_models.user import Users
from fastapi.exceptions import HTTPException


def access_token(db_session=Session, formData=formData):
    user = db_session.query(Users).filter(
        Users.email == formData.email).first()
    if not user:
        raise HTTPException(
            status_code=400, detail='No user found with your email ID')
    password = hashed_pwd(formData.password)
    if password != user.password:
        raise HTTPException(
            status_code=400, detail='Email and Password does not match')
    if user.user_id == 1:
        userRole = "admin"
    else:
        userRole = "user"
    payload = [{
        'user_id': user.user_id,
        'userRole': userRole
    }]
    access_token = jwt.encode({'data': payload},
                              'secret', algorithm='HS256')
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def login_type_access_token(db_session=Session, login_type=str, formData=loginTypeData):
    if not login_type == "google":
        user = db_session.query(Users).filter(
            Users.facebook_id == formData.facebook_id).first()
    else:
        user = db_session.query(Users).filter(
            Users.google_id == formData.google_id).first()
    if not user:
        user = Users(**formData.dict(exclude_unset=True))
        user.login_type = login_type
        user.created_on = datetime.now()
        return user_crud.save(db_session, user)
    if user.user_id == 1:
        userRole = "admin"
    else:
        userRole = "user"
    payload = [{
        'user_id': user.user_id,
        'userRole': userRole
    }]
    access_token = jwt.encode({'data': payload},
                              'secret', algorithm='HS256')
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def hashed_pwd(password):
    return hashlib.md5(password.encode()).hexdigest()
