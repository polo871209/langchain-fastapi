from fastapi import APIRouter

from . import question, summary, keyword

router = APIRouter(prefix="/bedrock", tags=["Bedrock"])

router.include_router(question.router)
router.include_router(summary.router)
# router.include_router(keyword.router)
