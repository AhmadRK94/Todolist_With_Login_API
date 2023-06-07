from fastapi import FastAPI, HTTPException, Depends, status
from . import models
from .db import engine
from .routers import todo, user, auth

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router)
app.include_router(todo.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"Hello": "Welcome to my api"}
