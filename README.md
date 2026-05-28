# Student Performance Tracker (SQL Relational Database)

## Name:
Lucky Eni

## Module Number:
SQL Relational Databases Module

## Date:
May 28, 2026

---

## 📌 Project Description
This project is a Python-based Student Performance Tracker that uses SQLite as a relational database. It allows users to manage students and their grades while demonstrating SQL operations including INSERT, UPDATE, DELETE, SELECT, JOIN, and aggregate functions.

---

## 💡 Features
- Add students
- Add grades
- Update grades
- Delete students and related grades
- View student reports using JOIN
- Perform aggregate analysis (AVG, COUNT, SUM)
- Filter data using date/time

---

## 🗄️ Database Design

### Tables:
#### Students
- id (Primary Key)
- name
- email
- created_at

#### Grades
- id (Primary Key)
- student_id (Foreign Key)
- subject
- score
- created_at

---

## 🔗 Relationships
- One student can have many grades
- grades.student_id references students.id

---

## ⚙️ How to Run

```bash
python app.py