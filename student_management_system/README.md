# Student Management System

A full-stack Student Management System mini-project based on the provided assessment requirements.

## Technologies

- HTML
- CSS
- JavaScript
- Python Flask
- SQLite
- REST API
- Fetch API / AJAX

## Features

- Add student
- View all students
- Search by name or roll number
- Update student details
- Delete student
- Duplicate roll number validation
- Marks validation (0-100)
- Contact validation
- Dynamic page updates without reload

## Project Structure

student_management_system/
│
├── app.py
├── requirements.txt
├── README.md
├── students.db          # created automatically after first run
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js

## How to Run

1. Open this folder in VS Code.
2. Open the terminal.
3. Create a virtual environment:

   python -m venv venv

4. Activate it on Windows:

   venv\Scripts\activate

5. Install Flask:

   pip install -r requirements.txt

6. Run:

   python app.py

7. Open the URL shown in the terminal, normally:

   http://127.0.0.1:5000

The SQLite database is created automatically.
