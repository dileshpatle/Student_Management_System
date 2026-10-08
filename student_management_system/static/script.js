const form = document.getElementById("studentForm");
const studentId = document.getElementById("studentId");
const nameInput = document.getElementById("name");
const rollNoInput = document.getElementById("rollNo");
const classInput = document.getElementById("studentClass");
const marksInput = document.getElementById("marks");
const contactInput = document.getElementById("contact");

const tableBody = document.getElementById("studentTable");
const searchInput = document.getElementById("search");
const message = document.getElementById("message");
const emptyMessage = document.getElementById("emptyMessage");

const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");


async function loadStudents(query = "") {
    const url = query
        ? `/api/students/search?q=${encodeURIComponent(query)}`
        : "/api/students";

    const response = await fetch(url);
    const students = await response.json();

    tableBody.innerHTML = "";

    if (students.length === 0) {
        emptyMessage.style.display = "block";
        return;
    }

    emptyMessage.style.display = "none";

    students.forEach(student => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${escapeHtml(student.name)}</td>
            <td>${escapeHtml(student.roll_no)}</td>
            <td>${escapeHtml(student.student_class)}</td>
            <td>${student.marks}</td>
            <td>${escapeHtml(student.contact)}</td>
            <td>
                <div class="action-buttons">
                    <button class="edit" onclick='editStudent(${JSON.stringify(student)})'>Edit</button>
                    <button class="delete" onclick="deleteStudent(${student.id})">Delete</button>
                </div>
            </td>
        `;

        tableBody.appendChild(row);
    });
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
        name: nameInput.value.trim(),
        roll_no: rollNoInput.value.trim(),
        student_class: classInput.value.trim(),
        marks: marksInput.value,
        contact: contactInput.value.trim()
    };

    const id = studentId.value;
    const method = id ? "PUT" : "POST";
    const url = id ? `/api/students/${id}` : "/api/students";

    const response = await fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        showMessage(result.error, true);
        return;
    }

    showMessage(result.message, false);
    resetForm();
    loadStudents();
});


function editStudent(student) {
    studentId.value = student.id;
    nameInput.value = student.name;
    rollNoInput.value = student.roll_no;
    classInput.value = student.student_class;
    marksInput.value = student.marks;
    contactInput.value = student.contact;

    formTitle.textContent = "Update Student";
    submitBtn.textContent = "Update Student";
    cancelBtn.classList.remove("hidden");

    window.scrollTo({ top: 0, behavior: "smooth" });
}


async function deleteStudent(id) {
    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    const response = await fetch(`/api/students/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    if (!response.ok) {
        showMessage(result.error, true);
        return;
    }

    showMessage(result.message, false);
    loadStudents(searchInput.value.trim());
}


cancelBtn.addEventListener("click", resetForm);


searchInput.addEventListener("input", () => {
    loadStudents(searchInput.value.trim());
});


function resetForm() {
    form.reset();
    studentId.value = "";

    formTitle.textContent = "Add Student";
    submitBtn.textContent = "Add Student";
    cancelBtn.classList.add("hidden");
}


function showMessage(text, isError) {
    message.textContent = text;
    message.style.color = isError ? "red" : "green";

    setTimeout(() => {
        message.textContent = "";
    }, 3000);
}


function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


loadStudents();
