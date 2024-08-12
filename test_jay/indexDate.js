document.addEventListener("DOMContentLoaded", function () {
  setDefaultDate();
});

function setDefaultDate() {
  const dateInput = document.getElementById("counseling-date");
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are zero-based
  const day = String(today.getDate()).padStart(2, "0");
  const todayString = `${year}-${month}-${day}`;
  dateInput.value = todayString;
}
