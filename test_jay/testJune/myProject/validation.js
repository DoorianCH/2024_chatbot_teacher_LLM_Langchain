import { getClientValue } from './formController.js';

export function validateInputs() {
    const date = document.getElementById('date').value;
    const contents = document.getElementById('contents').value;
    const method = document.getElementById('method').value;
    const client = getClientValue();

    if (!date) {
        alert("상담 날짜를 입력해주세요");
        return false;
    }
    if (!contents) {
        alert("상담 내용을 입력해주세요");
        return false;
    }
    if (!method) {
        alert("상담 방법을 선택해주세요");
        return false;
    }
    if (!client) {
        alert("상담자를 선택해주세요");
        return false;
    }
    return true;
}