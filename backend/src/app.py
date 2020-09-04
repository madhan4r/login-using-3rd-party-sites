from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .crud import user
from .db_models import user as db_model_user
from .models.user import UserBase, UserCreate, UserResponse, UserLogin


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


# @app.post("{login_type}/login/access-token", response_model=UserResponse)
# def access_token(user_data: UserLogin, db_session: Session = Depends(get_db)):
#     return True


@app.post("/user/create", response_model=UserResponse)
def create_job(user_data: UserCreate, db_session: Session = Depends(get_db)):
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
