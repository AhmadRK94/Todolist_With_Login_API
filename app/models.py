from .db import Base
from sqlalchemy import String, Integer, Boolean, TIMESTAMP, Column, text, ForeignKey
from sqlalchemy.orm import relationship


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
    content = Column(String, nullable=False)
    category = Column(String)
    status = Column(Boolean, nullable=False, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    owner = relationship("Users")
