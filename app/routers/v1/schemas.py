from typing import Optional

from pydantic import BaseModel


class QuestionBase(BaseModel):
    question: str


class Summary(QuestionBase):
    length: Optional[int] = 100


class KeyWord(QuestionBase):
    number: Optional[int] = 1


class Vertex(QuestionBase):
    pass


class Conversation(BaseModel):
    message: str
