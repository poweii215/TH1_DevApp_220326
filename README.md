# Todo User API

FastAPI project with:

- Cấp 0 — Làm quen FastAPI (Hello To-Do)
- Cấp 1 — CRUD cơ bản (dữ liệu trong RAM)
- Cấp 2 — Validation “xịn” + filter/sort/pagination
- Cấp 3 — Tách tầng (router/service/repository) + cấu hình chuẩn
- Cấp 4 — Dùng Database (SQLite/PostgreSQL) + ORM
- Cấp 5 — Authentication + User riêng
- Cấp 6 — Nâng cao (tag, deadline, nhắc việc)
- Cấp 7 — Testing + tài liệu + deploy
- Cấp 8 – Thêm một số tính năng

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

default:
GET /root

Authentication:
POST /auth/register
POST /auth/login
GET /auth/me


Todos:
POST /todos/
GET /todos/
GET /todos/{todo_id}
PUT /todos/{todo_id}
DELETE /todos/{todo_id}
PATCH /todos/{todo_id}/complete
GET /todos/status/overdue
GET /todos/status/today
