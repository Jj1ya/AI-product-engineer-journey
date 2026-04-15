from fastapi import FastAPI

from app.api.todo import router as todo_router

app = FastAPI(title="AI Product Engineer Day3 TODO API")


@app.get("/")
def read_root():
    return {"message": "Hello, AI Product Engineer!"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


app.include_router(todo_router)

from app.db.database import engine, Base
from app.db import models

models
Base.metadata.create_all(bind=engine)
