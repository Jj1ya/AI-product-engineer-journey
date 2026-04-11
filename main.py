from typing import Optional

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

app = FastAPI(title="AI Product Engineer Day2 TODO API")


# ---- Pydantic models ----
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Todo title")
    description: Optional[str] = Field(default=None, max_length=300)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=300)
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool


# ---- In-memory storage (DB 대신 임시 저장소) ----
todos: list[TodoResponse] = []
next_id = 1


@app.get("/")
def read_root():
    return {"message": "Hello, AI Product Engineer!"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate):
    global next_id

    todo = TodoResponse(
        id=next_id,
        title=payload.title,
        description=payload.description,
        completed=False,
    )
    todos.append(todo)
    next_id += 1
    return todo


@app.get("/todos", response_model=list[TodoResponse])
def list_todos():
    return todos


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int = Path(..., ge=1)):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(payload: TodoUpdate, todo_id: int = Path(..., ge=1)):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            updated = todo.model_copy(
                update={
                    "title": payload.title if payload.title is not None else todo.title,
                    "description": (
                        payload.description
                        if payload.description is not None
                        else todo.description
                    ),
                    "completed": (
                        payload.completed
                        if payload.completed is not None
                        else todo.completed
                    ),
                }
            )
            todos[idx] = updated
            return updated

    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int = Path(..., ge=1)):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(idx)
            return

    raise HTTPException(status_code=404, detail="Todo not found")