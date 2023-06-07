from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    username: str
    password: str


class Todo(BaseModel):
    content: str
    category: str
    status: bool = False


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True


class TodoResponse(BaseModel):
    # owner_id: int
    todo_id: int
    content: str
    category: str
    status: bool
    owner: UserResponse

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
