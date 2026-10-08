from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)
DATABASE = "students.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            student_class TEXT NOT NULL,
            marks REAL NOT NULL,
            contact TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


@app.route("/api/students/search", methods=["GET"])
def search_students():
    query = request.args.get("q", "").strip()

    conn = get_db_connection()
    students = conn.execute("""
        SELECT * FROM students
        WHERE name LIKE ? OR roll_no LIKE ?
        ORDER BY id DESC
    """, (f"%{query}%", f"%{query}%")).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()

    required = ["name", "roll_no", "student_class", "marks", "contact"]
    if not data or any(not str(data.get(field, "")).strip() for field in required):
        return jsonify({"error": "All fields are required."}), 400

    name = str(data["name"]).strip()
    roll_no = str(data["roll_no"]).strip()
    student_class = str(data["student_class"]).strip()
    contact = str(data["contact"]).strip()

    try:
        marks = float(data["marks"])
    except (ValueError, TypeError):
        return jsonify({"error": "Marks must be a number."}), 400

    if marks < 0 or marks > 100:
        return jsonify({"error": "Marks must be between 0 and 100."}), 400

    if not re.fullmatch(r"[0-9+\-\s]{7,15}", contact):
        return jsonify({"error": "Enter a valid contact number."}), 400

    conn = get_db_connection()

    try:
        conn.execute("""
            INSERT INTO students (name, roll_no, student_class, marks, contact)
            VALUES (?, ?, ?, ?, ?)
        """, (name, roll_no, student_class, marks, contact))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Roll number already exists."}), 409

    conn.close()
    return jsonify({"message": "Student added successfully."}), 201


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    required = ["name", "roll_no", "student_class", "marks", "contact"]
    if not data or any(not str(data.get(field, "")).strip() for field in required):
        return jsonify({"error": "All fields are required."}), 400

    name = str(data["name"]).strip()
    roll_no = str(data["roll_no"]).strip()
    student_class = str(data["student_class"]).strip()
    contact = str(data["contact"]).strip()

    try:
        marks = float(data["marks"])
    except (ValueError, TypeError):
        return jsonify({"error": "Marks must be a number."}), 400

    if marks < 0 or marks > 100:
        return jsonify({"error": "Marks must be between 0 and 100."}), 400

    if not re.fullmatch(r"[0-9+\-\s]{7,15}", contact):
        return jsonify({"error": "Enter a valid contact number."}), 400

    conn = get_db_connection()

    duplicate = conn.execute(
        "SELECT id FROM students WHERE roll_no = ? AND id != ?",
        (roll_no, student_id)
    ).fetchone()

    if duplicate:
        conn.close()
        return jsonify({"error": "Roll number already exists."}), 409

    cursor = conn.execute("""
        UPDATE students
        SET name = ?, roll_no = ?, student_class = ?, marks = ?, contact = ?
        WHERE id = ?
    """, (name, roll_no, student_class, marks, contact, student_id))

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found."}), 404

    return jsonify({"message": "Student updated successfully."})


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?", (student_id,)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found."}), 404

    return jsonify({"message": "Student deleted successfully."})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
