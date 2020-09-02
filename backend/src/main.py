from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import crud_login, db_model_login
from .model_login import UserCreate, UserUpdate


db_model_login.Base.metadata.create_all(bind=engine)

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


@app.post("/user/Create", response_model=UserCreate)
def create_job(user_data: UserCreate, db_session: Session = Depends(get_db)):
    return crud_login.create_user(db_session=db_session, user_data=user_data)


@app.get("/users/", response_model=List[UserCreate])
def get_all(skip: int = 0, limit: int = 10, db_session: Session = Depends(get_db)):
    return crud_login.get_all(db_session=db_session, skip=skip, limit=limit)


@app.get("/user/{user_id}", response_model=UserCreate)
def get_by_id(user_id: int, db_session: Session = Depends(get_db)):
    return crud_login.get_by_id(db_session=db_session, user_id=user_id)


@app.put("/user/{user_id}/Update", response_model=UserCreate)
def update_user(user_id: int, user_data: UserUpdate, db_session: Session = Depends(get_db)):
    return crud_login.update_user(db_session=db_session, user_id=user_id, user_data=user_data)
