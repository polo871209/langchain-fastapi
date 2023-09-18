from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException
from langchain import LLMChain, PromptTemplate
from sqlmodel import select

from app.database import GetAsyncSession
from app.models import Chat, ChatContent
from app.oauth import ApiAuth
from app.routers.v1.llm import chat_bison_llm
from app.routers.v1.schemas import Conversation

conversation_prompt = """
The following is a friendly conversation between a human and an AI.
Please response only the content of answer in plain text and without saying you are AI. {history}
next human question: {question}
"""

conversation_prompt_template = PromptTemplate(
    input_variables=["history", "question"], template=conversation_prompt
)

llm_chain = LLMChain(prompt=conversation_prompt_template, llm=chat_bison_llm)

router = APIRouter(prefix="/chat")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Create a new chat",
    description="This endpoint creates a new chat ID and returns it.",
)
async def create_chat(session: GetAsyncSession, auth: ApiAuth):
    """create new chat id"""
    new_chat = Chat()
    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)

    return {"chat_id": new_chat.id}


@router.post(
    "/{chat_id}",
    response_model=dict,
    summary="Interact with the chat bot",
    description="This endpoint allows you to chat with the AI. "
    "It takes a chat ID and a message as input and returns the AI's response.",
    responses={
        404: {"description": "Chat ID not found"},
        200: {"description": "Successful interaction with chatbot"},
    },
)
async def chat(
    session: GetAsyncSession,
    auth: ApiAuth,
    chat_id: int,
    payload: Conversation = Body(),
):
    check_chat_id_stmt = select(Chat).where(Chat.id == chat_id)
    check_chat_id = await session.exec(check_chat_id_stmt)
    if not check_chat_id.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"chat_id: {chat_id} does not exist.",
        )
    chat_history_stmt = (
        select(ChatContent)
        .where(ChatContent.chat_id == chat_id)
        .order_by(ChatContent.created_at)
    )
    chat_history = await session.exec(chat_history_stmt)

    # construct the history message
    messages = []
    for _chat in chat_history.all():
        auther = "human" if _chat.user else "ai"
        message_item = {"auther": auther, "message": _chat.content}
        messages.append(message_item)

    history_str = "\n".join([f"{msg['auther']}: {msg['message']}" for msg in messages])

    res = llm_chain.predict(history=history_str, question=payload.message)

    # add new message to db
    new_question = ChatContent(content=payload.message, user=True, chat_id=chat_id)
    session.add(new_question)

    # add new response to db
    new_ai_res = ChatContent(content=res, user=False, chat_id=chat_id)
    session.add(new_ai_res)
    await session.commit()

    # Add new question and response to messages list for the final response
    messages.append({"auther": "human", "message": payload.message})
    messages.append({"auther": "ai", "message": res})

    return {"messages": messages}
