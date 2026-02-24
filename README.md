# Todo User API

FastAPI project with:

- JWT Authentication
- User module
- Todo module
- Due date
- Tags
- Overdue / Today endpoints
- Testing with pytest
- Docker + PostgreSQL support

---

## 1. Run locally

pip install -r requirements.txt
uvicorn app.main:app --reload

Swagger:
http://localhost:8000/docs

---

## 2. Run test

pytest

---

## 3. Run with Docker

docker-compose up --build

App:
http://localhost:8000

---

## 4. API Endpoints

Auth:
POST /users/register
POST /users/login

Todo:
POST /todos/
GET /todos/
GET /todos/{id}
GET /todos/overdue
GET /todos/today
PUT /todos/{id}
DELETE /todos/{id}