# from datetime import datetime
#
# from sqlmodel import SQLModel, Field, create_engine, Session, select
# from fastapi import Depends, FastAPI, HTTPException, Query
#
#
# class ApiKey(SQLModel, table=True):
#     """API key."""
#     id: int = Field(default=None, primary_key=True)
#     api_key: str
#     created_at: datetime = Field(default=datetime.utcnow)
#
#
# class Chat(SQLModel, table=True):
#     """chat"""
#     id: int = Field(default=None, primary_key=True)
#     created_at: datetime = Field(default=datetime.utcnow)
#
#     # # Using List for relationship in SQLModel
#     # contents: List["DbChatContent"]
#
#
# class ChatContent(SQLModel, table=True):
#     """chat content"""
#     id: int = Field(default=None, primary_key=True)
#     content: str
#     user: bool  # 0-> AIMessage 1 -> HumanMessage
#     chat_id: int = Field(foreign_key='chat.id')
#     created_at: datetime = Field(default=datetime.utcnow)
#
#
# engine = create_engine("sqlite:///database.db", echo=True)
#
#
# def create_db_tables():
#     SQLModel.metadata.create_all(engine)
#
#
# create_db_tables()
#
#
# def get_session():
#     with Session(engine) as session:
#         yield session
#
#
# app = FastAPI()
#
#
# @app.get('/')
# def get_keys(session: Session = Depends(get_session)):
#     stmt = select(ApiKey)
#     return session.exec(stmt).all()
#     # return 'hi'
#
