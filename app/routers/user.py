from fastapi import status, APIRouter, HTTPException, Depends
from .. import models, schemas
from ..db import get_db
from ..utils import hash_password
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse]
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse
)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.user_id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id= {id} doesn't exist",
        )
    return user
