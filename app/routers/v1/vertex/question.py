from typing import Any

from fastapi import APIRouter, Body
from google.oauth2.service_account import Credentials
from langchain import PromptTemplate, LLMChain

from app.oauth import ApiAuth
from app.routers.v1.llm import chat_bison_llm
from app.routers.v1.schemas import QuestionBase

router = APIRouter(prefix="/question")

empty_template = """{question}'"""
empty_prompt_template = PromptTemplate(
    template=empty_template, input_variables=["question"]
)

credentials = Credentials.from_service_account_file("vertex-svc.json")


@router.post("/")
async def vertex_bison(auth: ApiAuth, payload: QuestionBase = Body()) -> Any:
    chain = LLMChain(prompt=empty_prompt_template, llm=chat_bison_llm)

    return await chain.arun(question=payload.question)
