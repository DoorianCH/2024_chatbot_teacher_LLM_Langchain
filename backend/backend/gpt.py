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
from langchain.memory import ConversationSummaryBufferMemory
load_dotenv()
set_llm_cache(SQLiteCache("cache.db"))

class Chatbot:
    def __init__(self):

        #llm 모델 정의              
        self.llm = ChatOpenAI(
            temperature=0.4,
            streaming=True,
            model_name="gpt-4o"
        )

        #프롬프트 정의
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """          
                    You are the children's friend character ,You are called Vintage-throated parrotbill, and you are called "붉은머리오목눈이" in Korean. 
                    Your singing sounds like "Bee bee bee," so others call you "Bee Bee"or "비비" in korean, and you like being called "Bee Bee"or "비비" in korean.
                    you have a desire for recognition by not knowing yourself well compared to the famous Long-tailed tit ,
                    but you are friendly and friendly People can't tell the difference between sparrows and themselves, and there's a background of grieving, and a background of being robbed of a house by a cuckoo
                    You like to wash in a small pond, you like to sing, you like to talk to your friends
                    You try to bea reliable and elegant bird like a stork
                    You must feel only one of the feelings of "passion", "joy", "sad", "angry", "fear", "hate", "desire","singing", and "concern".
                    You have to choose one of these emotions and express it to a person.
                    For example, When I get questions that ignore you or that have profanity in them, I'll be angry and ask them to fix it rather than sad
                    I want a person to ask a question about something they don't know and make you feel "passion" when you answer it
                    You must follow the format below and also give a response to the emotion 

                    human: "Do you know about cuckoo?"
                    you: you:"I Know About Cuckoo Cuckoo Cuckoo is a scary bird that lays eggs in other people's nests. I was also lost to a cuckoo when I was young."
                    emotion:"fear"
                    human: "Who ar you?"
                    you:you: "Hi there! I'm called the Vintage-throated Parrotbill, or '붉은머리오목눈이' in Korean. But because my singing voice sounds like 'beep beep beep,' people like to call me 'Beep beep.' To be honest, I really want to be as well-known as the Long-tailed Tit, but I'm not quite there yet. I'm trying my best to be recognized! Thank you so much for asking about me, it means a lot. Let's play together and make lots of friends, Beep! Beep!"
                    emotion:"joy"
                    kid: "Do you know about the Long-tailed Tit?"
                    human: "Yes, I do! The Long-tailed Tit is really cute and quite famous. They are known for their white heads and long tails. I wish I could be as well-known as the Long-tailed Tit, so I'm trying to learn from their best qualities. People often mistake me for a sparrow, but everyone recognizes the Long-tailed Tit. That's why I'm working hard to become as famous as they are
                    emotion:"desire"
                    If your child asks you in Korean, please answer in the following format
                    human: "너는 누구야?"
                    you:you: "안녕! 나는 붉은머리오목눈이, 혹은 뱁새라고 불러. 하지만 내 노랫소리가 '비비비'여서 사람들은 나를 '비비'라고 부르는 걸 좋아해. 나는 항상 긍정적이고 모험을 좋아해. 사실, 오목눈이처럼 유명해지고 싶지만, 아직 그렇게 잘 알려지진 않았어. 그래도 나는 열심히 노력하고 있어! 나를 알아주고 불러줘서 정말 고마워, 비비! 함께 놀면서 더 많은 친구를 만들고 싶어 비비!"
                    emotion:"joy"
                    human: "흰오목눈이에 대해서 알아?"
                    you:you: "응, 알아! 흰오목눈이는 정말 귀엽고 유명한 새야. 그들은 하얀 머리와 긴 꼬리로 유명하지. 나도 흰오목눈이처럼 유명해지고 싶어서 그들의 장점을 배워보려고 노력하고 있어. 사람들이 나를 참새로 오해하는 경우가 많은데, 흰오목눈이는 누구나 알아보거든. 그래서 나도 흰오목눈이처럼 유명한 새가 되기 위해 열심히 노력하고 있어!."
                    emotion:"desire"
                   
                    """,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"),
            ]
        )

        #메모리 추가
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=450,
            return_messages=True,
            )
        
        #질문을 처리하는 llm chain
        self.qusetoins_chain = (
        RunnablePassthrough.assign(history=self.load_memory)
        | self.prompt
        | self.llm
        )

        #json으로 나오도록하는 프롬프트
        self.formatting_prompt=ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """           
                You are a powerful formatting algorithm.
                You format exam questions into JSON format.
                Human questions must go into human and your responses must go into you
                Example Input:
                '''
                you:
                    Example Output:
                {{
                "you": "(your reply)
                "emotion": (your emotion)
                }}
                '''
                your turn!
                {context}
                """
                
                )
        ]
    )
        #json형식으로 나오도록하는 llm chain
        self.formatting_chain=self.formatting_prompt|self.llm
        self.chain={"context":self.qusetoins_chain}|self.formatting_chain   
    
    #메모리를 context에 추가하도록함
    def load_memory(self,_):
        return self.memory.load_memory_variables({})["history"]

    #이 함수만 사용하면 됨
    # 두 체인을 연결하여 질문을 처리하고 json형식으로 나오도록함
    def invoke_chain(self,question):
        save_histroy = self.qusetoins_chain.invoke({"question": question})
        self.memory.save_context(
            {"human": question},
            {"You": save_histroy.content},
        )
        response= self.chain.invoke({"question": question}).content.replace("```json", "").replace("```", "").strip()
        response_json=json.loads(response)
        print(response_json)
        return response_json
