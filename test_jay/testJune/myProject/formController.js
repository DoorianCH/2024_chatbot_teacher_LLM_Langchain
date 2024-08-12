export function toggleOtherInput() {
    const category = document.getElementById('category').value;
    const otherInput = document.getElementById('otherText');
    otherInput.readOnly = category !== "other";
    if (otherInput.readOnly) {
        otherInput.value = ''; 
    }
}

export function getClientValue() {
    const options = document.getElementsByName('client');
    for (const option of options) {
        if (option.checked) {
            return option.value;
        }
    }
}

export function getCategoryValue() {
    const category = document.getElementById('category').value;
    const otherInput = document.getElementById('otherText').value;
    return category === 'other' ? otherInput : category;
}

export function setTodayDate() {
    const dateInput = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
}