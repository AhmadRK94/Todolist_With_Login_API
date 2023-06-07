from fastapi import status, APIRouter, HTTPException, Depends
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..db import get_db
from typing import List

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.TodoResponse]
)
def get_all_todos(
    db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)
):
    todos = (
        db.query(models.Todos)
        .filter(models.Todos.owner_id == current_user.user_id)
        .all()
    )
    return todos


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoResponse
)
def create_todo(
    todo: schemas.Todo,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    new_todo = models.Todos(owner_id=current_user.user_id, **todo.dict())
    db.add(new_todo)
    db.commit()
    return new_todo


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.TodoResponse
)
def update_todo(
    input_todo: schemas.Todo,
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    todo = db.query(models.Todos).filter(
        models.Todos.todo_id == id, models.Todos.owner_id == current_user.user_id
    )
    if not todo.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id= {id} doesn't exist",
        )
    todo.update(input_todo.dict(), synchronize_session=False)
    db.commit()
    return todo.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    todo = db.query(models.Todos).filter(
        models.Todos.todo_id == id, models.Todos.owner_id == current_user.user_id
    )
    if not todo.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"todo with id= {id} doesn't exist",
        )
    todo.delete(synchronize_session=False)
    db.commit()
