import ast

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema.language_model import BaseLanguageModel

openai_llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)


class BasicChain:
    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm

    def empty_chain(self, question: str) -> str:
        """chain with no predefine prompt"""
        empty_template = """{question}'"""
        empty_prompt_template = PromptTemplate(
            template=empty_template, input_variables=["question"]
        )

        empty_chain = LLMChain(llm=self.llm, prompt=empty_prompt_template)
        return empty_chain.run(question=question)

    def translate_traditional_chinese_chain(self, text: str):
        """take a list of sting a translate into chinese"""
        translate_template = """
        given the text: '{text}',
        please translate to Traditional Chinese(Taiwan). Return the translated text only, and keep the origin format.
        """

        translate_prompt_template = PromptTemplate(
            input_variables=["text"], template=translate_template
        )

        translate_traditional_chinese_chain = LLMChain(
            llm=self.llm, prompt=translate_prompt_template
        )

        return translate_traditional_chinese_chain.run(text=text)

    def translate_traditional_summary_chinese_chain(self, text: str):
        """take a list of sting a translate into chinese"""
        translate_template = """
        given the information{information}, about a summary
        please translate to Traditional Chinese(taiwan)
        """

        translate_prompt_template = PromptTemplate(
            input_variables=["information"], template=translate_template
        )

        translate_traditional_chinese_chain = LLMChain(
            llm=self.llm, prompt=translate_prompt_template
        )

        return translate_traditional_chinese_chain.run(information=text)

    def to_python_list_chain(self, text: str) -> list:
        """take a list of sting a translate into chinese"""
        to_python_list_template = """
        given the string {string}, please convert it into a list format for example: ['keyword1', 'keyword2'] 
        and remove heading so I can return in my api response, please only return the list itself.
        """

        to_python_list__prompt_template = PromptTemplate(
            input_variables=["string"], template=to_python_list_template
        )

        to_python_list_chain = LLMChain(
            llm=self.llm, prompt=to_python_list__prompt_template
        )

        res = to_python_list_chain.run(string=text)
        print(res)
        return ast.literal_eval(res)
