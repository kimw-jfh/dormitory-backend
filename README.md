# University Dormitory Management System

A comprehensive dormitory management API built with FastAPI and SQLite. It provides user authentication, student records, room assignments, attendance tracking, and reservation handling.

## Features

- **Authentication** – Basic HTTP authentication with role-based access (admin, supervisor, student, financial)
- **Student Management** – Add, view, and list students
- **Room Management** – Add rooms, list all rooms, filter by status (available/occupied)
- **Attendance Recording** – Mark student attendance (admin/supervisor only) and retrieve attendance by date or student
- **Reservation System** – Students can request room reservations; admins can view pending requests and assign rooms
- **Persian Language Support** – All API messages and responses are in Persian

## Technologies

- Python 3.8+
- FastAPI – Web framework
- SQLite – Lightweight database
- Uvicorn – ASGI server
- Pydantic – Data validation

