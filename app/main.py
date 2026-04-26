from app.config import settings
from app.db import models
from app.db.database import Base, engine
from fastapi import FastAPI

from app.api.todo import router as todo_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)


@app.get("/")
def read_root():
    return {"message": "Hello, AI Product Engineer!"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


app.include_router(todo_router)