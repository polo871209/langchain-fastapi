from fastapi import APIRouter

from . import auth, openai, bedrock, vertex

router = APIRouter(
    prefix="/v1",
)

router.include_router(auth.router)
router.include_router(openai.router)
router.include_router(bedrock.router)
router.include_router(vertex.router)
