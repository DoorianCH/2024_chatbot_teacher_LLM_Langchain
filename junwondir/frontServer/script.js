let socket;
let userMessage = null; // 사용자가 입력한 메시지를 저장할 변수
// HTML 요소 선택자들을 정의
const closeBtn = document.querySelector(".close-btn");  // 챗봇 창 닫기 버튼
const chatbox = document.querySelector(".chatbox");  // 챗박스(대화 내용이 표시되는 영역)
const chatInput = document.querySelector(".chat-input textarea");  // 사용자가 메시지를 입력하는 텍스트 영역
const sendChatBtn = document.querySelector(".chat-input span");  // 사용자가 메시지를 전송하는 버튼

//ai가 응답시 해당 메시지를 이 변수에 저장해서 반화함 반환 전까지는 기다리라는 메시지가 나옴
let messageElement

// WebSocket으로부터 수신한 메시지를 처리하는 함수
const handleIncomingMessage = (data) => {
  try {
    const parsedData = JSON.parse(data);
    console.log(parsedData.message)
    messageElement.innerHTML=`${parsedData.message}`
  } catch (error) {
    console.error("Error parsing incoming message:", error);
  }
}

function connectWebSocket() {
  // WebSocket 연결을 설정합니다.
  socket = new WebSocket("ws://127.0.0.1:8000/chat");

  // WebSocket이 연결되었을 때 호출되는 이벤트 핸들러
  socket.onopen = function(event) {
      console.log("WebSocket connection established");
      document.getElementById("status").textContent = "WebSocket connected!";
  };

  // 서버로부터 메시지를 수신했을 때 호출되는 이벤트 핸들러
  socket.onmessage = function(event) {
    console.log(event.data)
    handleIncomingMessage(event.data);
  };

  // WebSocket이 닫혔을 때 호출되는 이벤트 핸들러
  socket.onclose = function(event) {
      console.log("WebSocket connection closed");
      document.getElementById("status").textContent = "WebSocket disconnected!";
  };

  // WebSocket 에러 발생 시 호출되는 이벤트 핸들러
  socket.onerror = function(error) {
      console.error("WebSocket error:", error);
      document.getElementById("status").textContent = "WebSocket error occurred!";
  };
}

window.onload = function() {
  connectWebSocket(); // 페이지 로드 시 WebSocket 연결
};


const inputInitHeight = chatInput.scrollHeight; // 텍스트 영역의 초기 높이를 저장

// API 설정
const API_KEY = "PASTE-YOUR-API-KEY"; // API 키를 여기에 입력 (실제 사용 시 API 키를 여기에 삽입)
const API_URL = `https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=${API_KEY}`; // API 요청을 보낼 URL

// 사용자가 입력한 메시지를 바탕으로 <li> 태그를 생성하는 함수
const createChatLi = (message, className) => {
  // 전달된 메시지와 클래스 이름을 사용하여 채팅 <li> 요소를 생성
  const chatLi = document.createElement("li");  // <li> 요소를 생성
  chatLi.classList.add("chat", `${className}`);  // 생성한 <li> 요소에 'chat' 및 전달된 클래스 이름을 추가
  let chatContent = className === "outgoing" 
    ? `<p></p>`  // 사용자가 보낸 메시지일 경우, <p> 태그만 추가
    : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;  // 챗봇의 응답일 경우, 아이콘과 <p> 태그 추가
  chatLi.innerHTML = chatContent;  // 생성된 HTML을 <li> 요소에 삽입
  chatLi.querySelector("p").textContent = message;  // <p> 태그 안에 메시지 텍스트를 삽입
  return chatLi; // 완성된 <li> 요소를 반환
}

// WebSocket을 통해 메시지를 보내고 응답을 처리하는 함수
const generateResponse = (chatElement) => {
  messageElement = chatElement.querySelector("p");  // 채팅 <li> 요소에서 <p> 요소를 선택

  // 서버로 전송할 메시지 구성 (JSON 형식)
  const message = {
    message: userMessage
  };

  // WebSocket을 통해 메시지를 서버로 전송
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(message));
  } else {
    // WebSocket 연결이 닫혀 있는 경우 처리
    messageElement.classList.add("error");
    messageElement.textContent = "WebSocket is not connected.";
    return;
  }

  // 수신 대기 메시지 표시
  messageElement.textContent = "Waiting for response...";
}

// 사용자의 채팅을 처리하는 함수
const handleChat = () => {
  userMessage = chatInput.value.trim(); // 사용자가 입력한 메시지를 가져오고, 불필요한 공백 제거
  if (!userMessage) return;  // 메시지가 없으면 종료

  // 입력 텍스트 영역을 비우고, 초기 높이로 되돌림
  chatInput.value = "";
  chatInput.style.height = `${inputInitHeight}px`;

  // 사용자의 메시지를 채팅박스에 추가
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  setTimeout(() => {
    // 응답을 기다리는 동안 "Thinking..." 메시지를 표시
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(incomingChatLi);  // 챗봇의 응답을 생성
  }, 600);  // 600ms 지연 후 실행
}

// 텍스트 영역의 내용에 따라 높이를 조정하는 이벤트 리스너
chatInput.addEventListener("input", () => {
  chatInput.style.height = `${inputInitHeight}px`;  // 초기 높이로 설정
  chatInput.style.height = `${chatInput.scrollHeight}px`;  // 텍스트 내용에 맞게 높이 조정
});

// 사용자가 Enter 키를 누를 때 이벤트 처리
chatInput.addEventListener("keydown", (e) => {
  // Shift 키 없이 Enter 키를 누르고, 창 너비가 800px보다 크면 채팅을 처리
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();  // 기본 Enter 키 동작(줄바꿈)을 막음
    handleChat();  // 채팅 처리 함수 호출
  }
});

// 전송 버튼을 클릭할 때 채팅 처리
sendChatBtn.addEventListener("click", handleChat);

// 닫기 버튼 클릭 시 챗봇 창 숨기기
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));



