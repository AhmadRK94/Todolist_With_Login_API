from .db import Base
from sqlalchemy import String, Integer, Boolean, TIMESTAMP, Column, text


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Todos(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String)
    status = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
