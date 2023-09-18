from fastapi import APIRouter

from . import question, summary, keyword

router = APIRouter(prefix="/openai", tags=["OpenAI"])

router.include_router(question.router)
router.include_router(summary.router)
router.include_router(keyword.router)
