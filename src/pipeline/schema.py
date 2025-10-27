from pydantic import BaseModel, Field
from typing import List, Any, Optional


# Pydantic class for Data Schema
class Content(BaseModel):
    type: str = "T"
    text: str


class Material(BaseModel):
    content: Content
    index: int


class Ask(BaseModel):
    type: str = "T"
    text: str = ""


class Choice(BaseModel):
    content: Content
    index: int
    isCorrect: bool


class Item(BaseModel):
    materials: List[Material] = Field(default_factory=list)
    ask: Ask = Field(default_factory=Ask)
    choices: List[Choice] = Field(default_factory=list)
    tags: List[Any] = Field(default_factory=list)
    difficulty: Optional[int] = None
    accuracy: Optional[int] = None
