from typing import Optional

from langchain import PromptTemplate, LLMChain
from langchain.chains import (
    ReduceDocumentsChain,
    MapReduceDocumentsChain,
    StuffDocumentsChain,
)
from langchain.chat_models import ChatOpenAI
from langchain.schema.language_model import BaseLanguageModel
from langchain.text_splitter import CharacterTextSplitter

openai_llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)


class KeywordChain:
    def __init__(
        self,
        llm: BaseLanguageModel,
        token_max: Optional[int] = 4000,
        chunk_size: Optional[int] = 1000,
    ):
        self.llm = llm
        self.token_max = token_max
        self.chunk_size = chunk_size

    def keyword(self, text: str, number: Optional[int] = 1) -> str:
        """chain with keyword prompt"""
        keyword_template = """
        Given the text "{text}", please provide exactly {number} keywords in a list format, for example: ['keyword1', 'keyword2'].
        """
        keyword_prompt_template = PromptTemplate(
            template=keyword_template, input_variables=["text", "number"]
        )

        empty_chain = LLMChain(llm=self.llm, prompt=keyword_prompt_template)
        return empty_chain.run(text=text, number=number)

    def longtext_keyword(self, text: str, number: int) -> str:
        """take a large input of text in map reduce and return a summary string in english"""
        # Map
        map_template = """TThe following set of documents is provided: {docs}.
        Please identify the main themes and provide as much information as possible.
        Helpful Answer:"""
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=self.llm, prompt=map_prompt)

        # Reduce
        tmp_reduce_template = "The following is a set of summaries:\n{doc_summaries}\n"
        keyword_template = f"Please provide exactly {number} keywords in a list format, for example: ['keyword1', 'keyword2']."
        reduce_template = f"{tmp_reduce_template}{keyword_template}"
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        reduce_chain = LLMChain(llm=self.llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="doc_summaries"
        )

        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=self.token_max,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size,
            chunk_overlap=0,
            separator="[。，\n\n]",
            is_separator_regex=True,
        )

        split_docs = text_splitter.create_documents([text])

        return map_reduce_chain.run(split_docs)
