document.addEventListener("DOMContentLoaded", function () {
  fetchStudents();
});

function fetchStudents() {
  fetch("data/students.json")
    .then((response) => response.json())
    .then((data) => {
      const sortedStudents = sortStudents(data.students);
      populateStudentSelect(sortedStudents);
    })
    .catch((error) => console.error("Error fetching student data:", error));
}

function sortStudents(students) {
  return students.sort((a, b) => a.localeCompare(b, "ko-KR"));
}

function populateStudentSelect(students) {
  const studentSelect = document.getElementById("student-name");
  students.forEach((student, index) => {
    const option = document.createElement("option");
    option.value = student;
    option.textContent = `${index + 1}. ${student}`;
    studentSelect.appendChild(option);
  });
}
