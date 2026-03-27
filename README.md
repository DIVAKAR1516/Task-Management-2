# Task Management REST API

## Features
- Create Task
- Get All Tasks
- Update Task Status
- Delete Task

## Tech Stack
- Django
- Django REST Framework
- PostgreSQL (for production)

## Setup Instructions

1. Clone repo
2. Create virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Run migrations:
   python manage.py migrate
5. Run server:
   python manage.py runserver

## API Endpoints

- GET /api/tasks/
- POST /api/tasks/
- PUT /api/tasks/{id}/
- DELETE /api/tasks/{id}/

## Author
Divakar