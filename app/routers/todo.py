from fastapi import status, APIRouter, HTTPException, Depends
from .. import models, schemas
from sqlalchemy.orm import Session
from ..db import get_db
from typing import List

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todos).all()
    return todos


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoResponse
)
def create_todo(todo: schemas.Todo, db: Session = Depends(get_db)):
    new_todo = models.Todos(**todo.dict())
    db.add(new_todo)
    db.commit()
    return new_todo


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_todo(input_todo: schemas.Todo, id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.todo_id == id)
    if not todo.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id= {id} doesn't exist",
        )
    todo.update(input_todo.dict(), synchronize_session=False)
    db.commit()
    return todo.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.todo_id == id)
    if not todo.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id= {id} doesn't exist",
        )
    todo.delete(synchronize_session=False)
    db.commit()
