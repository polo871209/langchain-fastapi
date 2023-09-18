from fastapi import APIRouter, Body, status
from langchain import LLMChain, PromptTemplate

from app.oauth import ApiAuth
from app.routers.v1.schemas import QuestionBase
from app.routers.v1.llm import bedrock_titan_llm

router = APIRouter(prefix="/question")

empty_template = """{question}"""
empty_prompt_template = PromptTemplate(
    input_variables=["question"], template=empty_template
)

chain = LLMChain(llm=bedrock_titan_llm, prompt=empty_prompt_template)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    summary="Empty prompt template 8k tokens.",
)
async def bedrock(auth: ApiAuth, payload: QuestionBase = Body()):
    """empty prompt template"""
    return await chain.arun(question=payload.question)
