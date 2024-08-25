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
    
        chatbot = Chatbot()  # Chatbot 인스턴스 생성
        while True:
            # 클라이언트로부터 메시지를 수신
            data = await websocket.receive_text()
            print(f"Received message: {data}")

        # 질문을 처리하고 토큰을 실시간으로 전송
            for token in chatbot.questions_chain.stream({"question": data}):
                await websocket.send_text(token.content)

    except WebSocketDisconnect:
        print("Client disconnected")