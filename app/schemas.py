from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    username: str
    password: str


class Todo(BaseModel):
    user_id: int
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
    user_id: int
    todo_id: int
    content: str
    category: str
    status: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
