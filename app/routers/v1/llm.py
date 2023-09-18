import boto3
from google.oauth2.service_account import Credentials
from langchain.chat_models import ChatOpenAI
from langchain.llms import VertexAI
from langchain.llms.bedrock import Bedrock


def get_bedrock_titan_llm() -> Bedrock:
    bedrock_client = boto3.client(
        "bedrock", "us-west-2", endpoint_url="https://bedrock.us-west-2.amazonaws.com"
    )
    bedrock_llm = Bedrock(model_id="amazon.titan-tg1-large", client=bedrock_client)
    return bedrock_llm


credentials = Credentials.from_service_account_file("vertex-svc.json")

openai_4k_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)
openai_16k_llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.5)
chat_bison_llm = VertexAI(model_name="text-bison@001", credentials=credentials)
bedrock_titan_llm = get_bedrock_titan_llm()
