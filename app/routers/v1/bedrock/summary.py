from fastapi import APIRouter, Body, status

from app.oauth import ApiAuth
from app.routers.v1.llm import bedrock_titan_llm, openai_4k_llm
from app.routers.v1.schemas import Summary
from app.utils.chains import SummaryChain, BasicChain
from app.utils.token_count import num_tokens_from_string

router = APIRouter(prefix="/summary")

summary_chain = SummaryChain(bedrock_titan_llm, token_max=6000, chunk_size=2000)
basic_chain = BasicChain(openai_4k_llm)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    summary="Generate Mandarin summary from question.",
)
def summary_text(auth: ApiAuth, payload: Summary = Body()) -> str:
    if num_tokens_from_string(payload.question) > 6000:
        # if text were too long use map reduce summary
        summary = summary_chain.longtext_summary(
            payload.question,
            length=payload.length,
        )
    else:
        summary = summary_chain.summary(payload.question, length=payload.length)

    # return summary
    return basic_chain.translate_traditional_summary_chinese_chain(summary)
