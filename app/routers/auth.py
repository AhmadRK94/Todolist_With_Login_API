from fastapi import status, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..utils import verify_password

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", status_code=status.HTTP_200_OK)
def user_login(user_input: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_input.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="wrong username or password!"
        )
    elif not verify_password(user_input.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="wrong username or password!"
        )
    else:
        return {"message": "Token send"}
