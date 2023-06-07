from jose import jwt, JWTError
from datetime import datetime, timedelta
from .config import setting
from fastapi.security import OAuth2PasswordBearer
from app import schemas, models
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from fastapi import HTTPException, status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=setting.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(
        to_encode, key=setting.secret_key, algorithm=setting.hash_algorithm
    )
    return jwt_token


def verify_access_token(token: str, credentials_execption):
    try:
        payload = jwt.decode(
            token=token, key=setting.secret_key, algorithms=setting.hash_algorithm
        )
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_execption
    except JWTError:
        raise credentials_execption
    token_data = schemas.TokenData(id=id)
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token=token, credentials_execption=credential_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user
