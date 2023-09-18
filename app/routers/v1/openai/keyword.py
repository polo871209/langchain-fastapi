from fastapi import APIRouter, Body, status, HTTPException

from app.oauth import ApiAuth
from app.routers.v1.llm import openai_16k_llm
from app.routers.v1.schemas import KeyWord
from app.utils.chains import KeywordChain, BasicChain
from app.utils.token_count import num_tokens_from_string

router = APIRouter(prefix="/keyword")

keyword_chain = KeywordChain(openai_16k_llm, token_max=12000, chunk_size=4000)
basic_chain = BasicChain(openai_16k_llm)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Generate Mandarin keyword from question",
)
def keyword_text(auth: ApiAuth, payload: KeyWord = Body()) -> list:
    try:
        if num_tokens_from_string(payload.question) > 8000:
            # if text were too long use map reduce summary
            keyword = keyword_chain.longtext_keyword(payload.question, payload.number)
        else:
            keyword = keyword_chain.keyword(payload.question, payload.number)
        translated_keyword = basic_chain.translate_traditional_chinese_chain(keyword)

        return basic_chain.to_python_list_chain(translated_keyword)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an issue processing the AI's response. Please try again.",
        )
