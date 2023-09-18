# from fastapi import APIRouter, Body, status, HTTPException
#
# from app.oauth import ApiAuth
# from app.routers.v1.llm import bedrock_titan_llm, openai_4k_llm
# from app.routers.v1.schemas import KeyWord
# from app.utils.chains import KeywordChain, BasicChain
# from app.utils.token_count import num_tokens_from_string
#
# router = APIRouter(prefix="/keyword")
#
# keyword_chain = KeywordChain(bedrock_titan_llm, token_max=6000, chunk_size=2000)
# basic_chain = BasicChain(openai_4k_llm)
#
#
# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     summary="Generate Mandarin keyword from question",
# )
# def keyword_text(auth: ApiAuth, payload: KeyWord = Body()) -> list:
#     try:
#         if num_tokens_from_string(payload.question) > 6000:
#             # if text were too long use map reduce summary
#             keyword = keyword_chain.longtext_keyword(payload.question, payload.number)
#         else:
#             keyword = keyword_chain.keyword(payload.question, payload.number)
#         translated_keyword = basic_chain.translate_traditional_chinese_chain(keyword)
#
#         return basic_chain.to_python_list_chain(translated_keyword)
#
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="There was an issue processing the AI's response. Please try again.",
#         )
