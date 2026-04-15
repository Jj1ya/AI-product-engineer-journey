from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
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




from pydantic import BaseModel, ConfigDict

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    model_config = ConfigDict(from_attributes=True)
    