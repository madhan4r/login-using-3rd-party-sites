from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .crud import user, login, apartments, joinApartments
from .db_models import user as db_model_user
from .models.user import UserBase, UserCreate, UserResponse
from .models.login import formData, loginTypeData
from .models.apartments import ApartmentResponse, ApartmentBase
from .models.joinApartments import JoinApartmentBase, JoinApartmentResponse

db_model_user.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/access-token")
def access_token(formData: formData, db_session: Session = Depends(get_db)):
    return login.access_token(db_session=db_session, formData=formData)


@app.post("/{login_type}/user/access-token",)
def login_type_access_token(formData: loginTypeData, login_type: str, db_session: Session = Depends(get_db)):
    return login.login_type_access_token(db_session=db_session, login_type=login_type, formData=formData)


@app.post("/user/create", response_model=UserResponse)
def create_user(user_data: UserCreate, db_session: Session = Depends(get_db)):
    return user.create_user(db_session=db_session, user_data=user_data)


@app.get("/users/", response_model=List[UserResponse])
def get_all(skip: int = 0, limit: int = 10, db_session: Session = Depends(get_db)):
    return user.get_all(db_session=db_session, skip=skip, limit=limit)


@app.get("/user/{user_id}", response_model=UserResponse)
def get_by_id(user_id: int, db_session: Session = Depends(get_db)):
    return user.get_by_id(db_session=db_session, user_id=user_id)


@app.put("/user/{user_id}/Update", response_model=UserResponse)
def update_user(user_id: int, user_data: UserBase, db_session: Session = Depends(get_db)):
    return user.update_user(db_session=db_session, user_id=user_id, user_data=user_data)


@app.post("/apartments/create", response_model=ApartmentResponse)
def create_apartment(apartment_data: ApartmentBase, db_session: Session = Depends(get_db)):
    return apartments.create_apartment(db_session=db_session, apartment_data=apartment_data)


@app.get("/apartments/", response_model=List[ApartmentResponse])
def get_all(skip: int = 0, limit: int = 10, db_session: Session = Depends(get_db)):
    return apartments.get_all(db_session=db_session, skip=skip, limit=limit)


@app.post("/apartments/join", response_model=JoinApartmentResponse)
def join_apartment(joinApartment_data: JoinApartmentBase, db_session: Session = Depends(get_db)):
    return joinApartments.join_apartment(db_session=db_session, joinApartment_data=joinApartment_data)
