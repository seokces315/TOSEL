from pydantic import BaseModel, Field
from typing import List, Any, Optional


# Pydantic class for Data Schema
class Content(BaseModel):
    type: str
    text: str


class Choice(BaseModel):
    content: Content
    index: int
    isCorrect: bool


class Material(BaseModel):
    content: Content
    index: int


class Ask(BaseModel):
    type: str
    text: str


class Item(BaseModel):
    choices: List[Choice]
    materials: List[Material] = Field(default_factory=list)
    tags: List[Any] = Field(default_factory=list)
    ask: Ask
    difficulty: Optional[int] = None
    accuracy: Optional[int] = None
