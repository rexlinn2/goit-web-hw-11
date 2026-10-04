# GoIT Web Homework 11 — Contacts API

REST API для керування контактами на FastAPI, SQLAlchemy 2 та PostgreSQL.

## Можливості
- CRUD: створення, перегляд, оновлення та видалення контактів.
- Пошук за ім'ям, прізвищем або email через query-параметр `search`.
- Список днів народження на найближчі 7 днів.
- Валідація даних через Pydantic.
- Автоматична документація Swagger UI та ReDoc.

## Запуск на Windows (PowerShell)

1. Створіть та активуйте віртуальне середовище:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Встановіть залежності:
   ```powershell
   pip install -r requirements.txt
   ```
3. Запустіть PostgreSQL через Docker (потрібен встановлений Docker Desktop):
   ```powershell
   docker compose up -d
   ```
4. За потреби скопіюйте `.env.example` у `.env`. Значення за замовчуванням відповідає docker-compose.
5. Запустіть API:
   ```powershell
   uvicorn main:app --reload
   ```

Відкрийте http://127.0.0.1:8000/docs для Swagger UI або http://127.0.0.1:8000/redoc для ReDoc.

## Ендпоїнти

| Метод | Шлях | Призначення |
|---|---|---|
| POST | `/api/contacts/` | Створити контакт |
| GET | `/api/contacts/` | Список контактів |
| GET | `/api/contacts/?search=anna` | Пошук |
| GET | `/api/contacts/birthdays` | Дні народження на найближчі 7 днів |
| GET | `/api/contacts/{contact_id}` | Отримати контакт |
| PUT | `/api/contacts/{contact_id}` | Оновити контакт |
| DELETE | `/api/contacts/{contact_id}` | Видалити контакт |

Приклад JSON для створення:
```json
{
  "first_name": "Anna",
  "last_name": "Smith",
  "email": "anna@example.com",
  "phone": "+380501234567",
  "birthday": "1995-04-20",
  "additional_data": "Колега"
}
```

`email` має бути унікальним. Для відсутнього контакту API повертає 404, для дубльованої адреси — 409.
