from fastapi import APIRouter

from . import question, chat

router = APIRouter(prefix="/vertex", tags=["Vertex"])

router.include_router(question.router)
router.include_router(chat.router)
