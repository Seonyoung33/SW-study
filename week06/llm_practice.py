from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
import os
import time
import shutil

output_parser = StrOutputParser()

api_key = "" # api키
path = "test_data"

def create_chroma_db(persist_direc, documents): # 크로마 임베딩 생성.
    embedding = OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-3-small")
    db = Chroma.from_documents(documents, embedding=embedding, persist_directory=persist_direc)
    
    return db


def response_ensemble_retriever(db: Chroma, docs, user_input): # 앙상블 리트리버
    filtered_docs = docs
    filtered_db = db

    vector_retriever = filtered_db.as_retriever(search_kwargs={"k": 2})
    bm25_retriever = BM25Retriever.from_documents(filtered_docs)
    bm25_retriever.k = 2

    ensemble_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.5, 0.5]
    )

    document = ensemble_retriever.invoke(user_input)
    
    return document
    


loader = TextLoader(os.path.join(path, 'test_week6.txt'), "utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len
)

split_docs = text_splitter.split_documents(documents)
formed_documents = split_docs[0].page_content

openai_mini = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18",
                        streaming=True,
                        temperature = 0,
                        openai_api_key=api_key)


def create_response_chain(llm):
    system_message = '''
당신은 의약품에 대해 전문적인 지식을 가진 약사입니다.

사용자는 의약품에 대한 질문을 하며, 해당 의약품에 대한 자세한 정보를 제공해야 합니다.
의약품 문서를 참조하여, 정확한 정보를 제공하세요.

사용자의 질문: "{user_input}"
의약품 문서: "[{formed_documents}]"
답변: ""
'''

    #해당 부서를 분류하기 위한 체인
    rephrase_prompt = PromptTemplate(
        template=system_message,
        input_variables=["user_input", "formed_documents"],
    )
    distribution_chain = rephrase_prompt | llm | output_parser
    return distribution_chain

model_response = create_response_chain(openai_mini)


def create_feedback_chain(llm):
    system_message = '''
당신은 의약품에 관한 ai의 답변에서 부족한 점을 피드백을 주는 전문적인 약사입니다.

'사용자의 질문'을 바탕으로 'ai의 답변'이 생성되었으며, 참조한 문서는 '의약품 문서'입니다.

[피드백 분석 과정]
1. '사용자의 질문'에 대해 답변을 하기 위한 정보가 '의약품 문서'에 들어있나요?
2. '사용자의 잘문'에 대해 'ai의 답변'은 사용자에게 충분한 정보를 전달하나요?
3. '의약품 문서'를 바탕으로 'ai의 답변'이 생성되었나요?

다음 피드백 분석 과정을 통해 보완할 점을 자세하게 작성하세요.

사용자의 질문: "{user_input}"
의약품 문서: "[{formed_documents}]"
ai의 답변: "{ai_response}"
피드백: ""
'''

    #해당 부서를 분류하기 위한 체인
    rephrase_prompt = PromptTemplate(
        template=system_message,
        input_variables=["user_input", "formed_documents", "ai_response"],
    )
    distribution_chain = rephrase_prompt | llm | output_parser
    return distribution_chain

model_feedback = create_feedback_chain(openai_mini)





def get_response(user_input):
    response = model_response.invoke({"user_input": user_input, "formed_documents": formed_documents})
    print(response)
    return response

def get_feedback(user_input, ai_response):
    feedback = model_feedback.invoke({"user_input": user_input, "formed_documents": formed_documents, "ai_response": ai_response})
    print(feedback)
    return feedback

# print(response)