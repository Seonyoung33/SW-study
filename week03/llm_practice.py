from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

output_parser = StrOutputParser()

api_key = "" # api키
path = "test_data"
loader = TextLoader(os.path.join(path, 'test_week3.txt'), "utf-8")


openai_mini = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18",
                        streaming=True,
                        temperature = 0,
                        openai_api_key=api_key)

def create_onoff_summarize_chain(llm):
    system_message = '''
당신은 전문적인 지식을 가진 뛰어난 사육사입니다.

주어진 문서를 바탕으로 사용자의 질문에 정확하게 답변하세요:

사용자의 질문: "{user_input}"
'''

    #해당 부서를 분류하기 위한 체인
    rephrase_prompt = PromptTemplate(
        template=system_message,
        input_variables=["user_input"],
    )
    distribution_chain = rephrase_prompt | llm | output_parser
    return distribution_chain

model = create_onoff_summarize_chain(openai_mini)

user_input = input("질문을 입력하세요:")
response = model.invoke({"user_input": user_input})

print(response)