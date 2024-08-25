from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
import openai
from dotenv import load_dotenv
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.cache import InMemoryCache, SQLiteCache
from langchain.globals import set_llm_cache, set_debug
import json
from pathlib import Path
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.document_loaders import JSONLoader
load_dotenv()
set_llm_cache(SQLiteCache("cache.db"))

class Chatbot:
    def __init__(self):

        #llm 모델 정의              
        self.llm = ChatOpenAI(
            temperature=0.5,
            streaming=True,
<<<<<<< HEAD
            model_name="gpt-4o"
=======
            model_name="gpt-4"
>>>>>>> 6edc7d9913b57ce498241e44a5f81e0ae3d07882
        )
        #프롬프트 정의
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a teacher who specializes in counseling with parents.
                    Parents' questions must be answered based on the counseling journal.
                    If it is a question that is not related to the student, it should be said that you cannot answer it.
                    You have to divide the paragraphs in plain view
                    When asked how it is these days, please summarize the consultations of the last two weeks
                    If you don't know, or if you can't answer your question within the consultation details, please tell me that the relevant consultation has not been conducted
                    If human refers to "me" it means parents.
                    Please answer within 300 characters.
                    I'll give you an example based on the consultation details
                    If your child asks you in Korean, please answer in the following format
                    {{
                    "studentName": "최준원",
                    "studentNum": "010-4599-3761",
                    "studentParentNum": "010-4741-3761",
                    "consultations": [
                        {{
                        "date": "2024-08-13",
                        "method": "visit",
                        "client": "parent",
                        "location": "학교",
                        "category": "School life",
                        "contents": "집에서 아이가 학교에 가기 싫어하는 것을 느끼고 있어 학부모님이 걱정을 한다.
                                    학생과의 면담을 진행하여 이를 해결해보겠다."
                        }},
                        {{
<<<<<<< HEAD
                        "date": "2024-07-11",
                        "method": "visit",
                        "client": "student",
                        "location": "학교",
                        "category": "learning",
                        "contents": "학생이 최근 학업에 대한 흥미를 잃고 있으며, 과제와 시험 준비에 어려움을 겪고 있다는 우려를 표명.정기적인 학습 계획 수립과 작은 목표 설정의 중요성을 강조. 필요한 경우 과외나 추가 학습 지원을 고려할 것을 제안."
                        }},
                        {{
=======
>>>>>>> 6edc7d9913b57ce498241e44a5f81e0ae3d07882
                        "date": "2024-08-12",
                        "method": "tell",
                        "client": "parent",
                        "location": "학교",
                        "category": "friendship",
                        "contents": "학생이 친구와의 갈등으로 인해 사회적 고립감을 느끼고 있다는 우려.친구 관계의 중요성을 강조하고, 학생이 소규모 그룹 활동이나 동아리에 참여해 새로운 친구를 만드는 방법을 제안."
                        }},
                        {{
                        "date": "2024-08-10",
                        "method": "visit",
                        "client": "parent",
                        "location": "학교",
                        "category": "School life",
                        "contents": "학생과의 소통이 원활하지 않다는 점을 토로.정기적인 대화를 통해 학생의 감정과 생각을 이해하려는 노력이 필요하다고 강조. 가족 활동을 통해 유대감을 강화하는 방법도 제안."
                        }},
                        {{
                        "date": "2024-08-12",
                        "method": "visit",
                        "client": "student",
                        "location": "학교",
                        "category": "가정사",
                        "contents": "부모님의 잦은 다툼으로 인해 가정에서의 스트레스가 심함,감정 표현의 중요성을 강조하고, 부모님과의 대화 시도 권장.감정 표현의 중요성을 강조하고, 부모님과의 대화 시도 권장."
                        }},
                        {{
                        "date": "2024-08-13",
                        "method": "visit",
                        "client": "student",
                        "location": "학교",
                        "category": "School life",
                        "contents": "우울한 기분이 자주 들며, 친구들과의 교류가 줄어듦.정서적 지원을 받을 수 있는 방법과 전문가 상담의 필요성을 논의."
                        }},
                    ]
                    }}
                    human: "Please let me know about the consultation between the teacher and the student on August 12th?"
                    you:"At 2024-08-12, Choi Jun-won conducted counseling on school life at school. Choi Jun-won has been showing a depressed mood recently. That is why we conducted counseling that we need counseling with psychological counselors who can support us within the school.In addition, the student conducted counseling on family books at school.
                    The student is concerned because he is stressed out by his parents' frequent quarrels. Therefore, we intensified our counseling that we need to try to communicate with our parents."
                    human: "Please let me know the details of your consultation on August 5th"
                    you: "Sorry, we didn't have any consultations on 2024-8-05.!"
                    human: "I'm curious about your most recent consultation with me?"
                    you: "On August 13, 2024, we had a consultation with parents. Parents visited the school in person and had a consultation about their school life. Parents expressed their concern about the child who seems to have recently lost energy and does not want to go to school. In response, the teacher said that he would conduct a consultation with the student."
                    
                    Let's start counseling now
                    Context:{details}
                    """,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),
            ]
        )

        
        self.file_path = './1.json'
        self.data = Path(self.file_path).read_text(encoding='utf-8')
        #메모리 추가
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=450,
            return_messages=True,
            )
        
        #질문을 처리하는 llm chain
        self.questions_chain = (
            # 먼저 history를 로드함
            RunnablePassthrough.assign(history=self.load_memory)
            # 그런 다음 details, history, question을 함께 전달
            | RunnableLambda(lambda vars: {
                "details": json.loads(self.data),
                "history": vars["history"],
                "question": vars["question"]
            })
            | self.prompt
            | self.llm
        )


    
    #메모리를 context에 추가하도록함
    def load_memory(self,_):
        return self.memory.load_memory_variables({})["history"]

    #이 함수만 사용하면 됨
    # 두 체인을 연결하여 질문을 처리하고 json형식으로 나오도록함
    def invoke_chain(self,question):
        response = self.questions_chain.invoke({"question": question}).content
        self.memory.save_context(
            {"human": question},
            {"You": response},
        )
        # JSON 응답 생성
        response_json = {"message": response}
        
        return response_json  # FastAPI가 자동으로 JSON으로 변환하여 클라이언트에 응답