from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from gpt import Chatbot
from fastapi import FastAPI, WebSocket
# 데이터 모델 정의
class Message(BaseModel):
    message: str

app = FastAPI()

# CORS 미들웨어 설정
origins = [
    "http://localhost",
    "http://localhost:3000/chatbot",
    "https://toro-backend.vercel.app/",
     "http://localhost:3001",
     "http://127.0.0.1:5500/index.html"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
    
        chatbot_instance = Chatbot()  # Chatbot 인스턴스 생성
        while True:
            # 클라이언트로부터 메시지를 수신
            data = await websocket.receive_text()
            print(f"Received message: {data}")

            # LLM에 메시지 전달 및 응답 생성
            response = chatbot_instance.invoke_chain(data)
            print(response)
            # 응답을 클라이언트로 전송
            await websocket.send_json(response)

    except WebSocketDisconnect:
        print("Client disconnected")