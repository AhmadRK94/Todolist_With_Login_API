from fastapi import status, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..utils import verify_password
from app.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", status_code=status.HTTP_200_OK)
def user_login(
    user_input: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # def user_login(user_input: schemas.UserLogin, db: Session = Depends(get_db)):
    # user = db.query(models.Users).filter(models.Users.email == user_input.email).first()
    user = (
        db.query(models.Users).filter(models.Users.email == user_input.username).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="wrong username or password!"
        )
    elif not verify_password(user_input.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="wrong username or password!"
        )
    else:
        access_token = create_access_token(data={"user_id": user.user_id})
        token = schemas.Token(access_token=access_token, token_type="bearer")
        return token
