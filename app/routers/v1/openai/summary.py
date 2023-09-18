from fastapi import APIRouter, Body, status

from app.oauth import ApiAuth
from app.routers.v1.llm import openai_16k_llm
from app.routers.v1.schemas import Summary
from app.utils.chains import SummaryChain, BasicChain
from app.utils.token_count import num_tokens_from_string

router = APIRouter(prefix="/summary")

summary_chain = SummaryChain(openai_16k_llm, token_max=12000, chunk_size=4000)
basic_chain = BasicChain(openai_16k_llm)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    summary="Generate Mandarin summary from question...",
)
def summary_text(auth: ApiAuth, payload: Summary = Body()) -> str:
    if num_tokens_from_string(payload.question) > 8000:
        # if text were too long use map reduce summary
        summary = summary_chain.longtext_summary(
            payload.question,
            length=payload.length,
        )
    else:
        summary = summary_chain.summary(payload.question, length=payload.length)

    return basic_chain.translate_traditional_summary_chinese_chain(summary)
