from sqlalchemy import Boolean, Column, Integer, String

from app.db.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(300), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)