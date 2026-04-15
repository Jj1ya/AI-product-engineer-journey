from fastapi import APIRouter, Path

from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])
todo_service = TodoService()


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate):
    return todo_service.create(payload)


@router.get("", response_model=list[TodoResponse])
def list_todos():
    return todo_service.list_all()


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int = Path(..., ge=1)):
    return todo_service.get_by_id(todo_id)


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(payload: TodoUpdate, todo_id: int = Path(..., ge=1)):
    return todo_service.update(todo_id, payload)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int = Path(..., ge=1)):
    todo_service.delete(todo_id)
    return







from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    return todo_service.create(db, payload)