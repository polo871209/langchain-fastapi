from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class ApiKey(SQLModel, table=True):
    """API key."""

    id: Optional[int] = Field(default=None, primary_key=True)
    api_key: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Chat(SQLModel, table=True):
    """chat"""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # # Using List for relationship in SQLModel
    # contents: List["DbChatContent"]


class ChatContent(SQLModel, table=True):
    """chat content"""

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    user: bool  # 0-> AIMessage 1 -> HumanMessage
    chat_id: int = Field(foreign_key="chat.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
