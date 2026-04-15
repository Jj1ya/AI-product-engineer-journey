from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    def create(self, db: Session, payload: TodoCreate) -> Todo:
        todo = Todo(
            title=payload.title,
            description=payload.description,
            completed=False,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def list_all(self, db: Session) -> list[Todo]:
        return db.query(Todo).all()

    def get_by_id(self, db: Session, todo_id: int) -> Todo:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    def update(self, db: Session, todo_id: int, payload: TodoUpdate) -> Todo:
        todo = self.get_by_id(db, todo_id)

        if payload.title is not None:
            todo.title = payload.title
        if payload.description is not None:
            todo.description = payload.description
        if payload.completed is not None:
            todo.completed = payload.completed

        db.commit()
        db.refresh(todo)
        return todo

    def delete(self, db: Session, todo_id: int) -> None:
        todo = self.get_by_id(db, todo_id)
        db.delete(todo)
        db.commit()