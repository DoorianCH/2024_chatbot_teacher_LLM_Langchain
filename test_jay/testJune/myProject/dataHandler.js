// dataHandler.js

import { getClientValue, getCategoryValue } from './formController.js';
import { validateInputs } from './validation.js';

let studentData = {
    studentName: "김일번",
    studentNum: "010-4599-3761",
    studentParentNum: "010-4741-3761",
    consultations: []
};

// 초기화 시 데이터 불러오기
function loadStudentData() {
    const storedData = localStorage.getItem('studentData');
    if (storedData) {
        studentData = JSON.parse(storedData);
    } else {
        studentData.consultations = []; // 상담 내역 초기화
    }
}

// 초기화 시 로컬 스토리지 비우기 (필요 시)
//localStorage.removeItem('studentData');

export function createJsonData() {
    const method = document.getElementById("method").value;
    const client = getClientValue();
    const category = getCategoryValue();
    const date = document.getElementById("date").value;
    const location = document.getElementById("location").value || "학교";
    const contents = document.getElementById("contents").value;

    const consultation = {
        date: date,
        method: method,
        client: client,
        location: location,
        category: category,
        contents: contents
    };

    // 새로운 날짜의 상담 데이터를 배열 맨 앞에 추가
    studentData.consultations.unshift(consultation);

    // 로컬 스토리지에 저장
    localStorage.setItem('studentData', JSON.stringify(studentData));

    return studentData;
}

export function saveConsultationData() {
    if (!validateInputs()) {
        return;
    }

    createJsonData();

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:3000/save_data", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                alert("상담 내용이 성공적으로 저장되었습니다.");
            } else {
                alert("상담 데이터를 저장하는 중 오류가 발생했습니다.");
            }
        }
    };

    xhr.send(JSON.stringify(studentData));
}

export function renderConsultationList() {
    const consultationList = document.getElementById('consultationList');
    consultationList.innerHTML = ''; // 기존 내용을 초기화

    studentData.consultations.forEach((consultation) => {
        const consultationItem = document.createElement('div');
        consultationItem.className = 'consultation-item';
        consultationItem.innerHTML = `
            <p><strong>날짜:</strong> ${consultation.date}</p>
            <p><strong>상담내용:</strong> ${consultation.contents}</p>
            <hr>
        `;
        consultationList.appendChild(consultationItem);
    });
}

// 초기화 시 데이터 불러오기
loadStudentData();
