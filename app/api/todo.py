from typing import Generator

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])
todo_service = TodoService()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    return todo_service.create(db, payload)


@router.get("", response_model=list[TodoResponse])
def list_todos(db: Session = Depends(get_db)):
    return todo_service.list_all(db)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return todo_service.get_by_id(db, todo_id)


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(payload: TodoUpdate, todo_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return todo_service.update(db, todo_id, payload)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    todo_service.delete(db, todo_id)
    return