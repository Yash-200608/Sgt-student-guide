# SGT Navigator Backend

SGT Navigator is a production-style university dashboard backend built with FastAPI and MongoDB. It exposes REST APIs for university dashboard data, authentication, personalization, admin management, search, notifications, attendance, transport, and analytics.

The codebase follows a route -> service -> database flow. Route handlers stay thin, service modules own business/database logic, schemas validate payloads, and shared concerns live in `config`, `security`, `dependencies`, `middleware`, and `utils`.

## Tech Stack

- FastAPI
- Uvicorn
- MongoDB Atlas
- Motor async MongoDB driver
- Pydantic
- bcrypt password hashing
- PyJWT access tokens
- python-dotenv

## Folder Structure

```text
backend/
  app/
    main.py                  FastAPI app factory, CORS, routes, lifecycle, errors
    config/                  Settings, MongoDB connection, indexes
    dependencies/            Auth and role dependencies
    middleware/              Security headers
    routes/                  HTTP route modules
    schemas/                 Pydantic request/response models
    security/                Password hashing and JWT helpers
    services/                Async business and MongoDB logic
    utils/                   Response, update, and ObjectId helpers
  requirements.txt
  README.md
  run.py
```

## Installation

Use Python 3.11 or newer.

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env`.

```powershell
Copy-Item .env.example .env
```

Configure:

```env
MONGO_URL=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
DATABASE_NAME=sgt_navigator
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOW_ADMIN_SIGNUP=false
```

`MONGO_URL` and `JWT_SECRET_KEY` are required at runtime. Use a long random secret for JWT signing. Keep `ALLOW_ADMIN_SIGNUP=false` outside controlled local setup; seed the first admin directly in MongoDB or temporarily enable it in a trusted environment.

## MongoDB Setup

Create a MongoDB Atlas cluster and allow the app IP in network access. The app creates indexes on startup for users, timetable, events, notices, teachers, clubs, bookmarks, preferences, notifications, attendance, and bus routes.

Collections used:

- `users`
- `timetable`
- `events`
- `notices`
- `teachers`
- `clubs`
- `bookmarks`
- `preferences`
- `notifications`
- `attendance`
- `bus_routes`

## Running the Server

```bash
python run.py
```

Alternative:

```bash
uvicorn app.main:app --reload
```

Docs:

```text
http://localhost:8000/docs
```

Health:

```text
GET /api/health
```

## Authentication

Signup:

```http
POST /api/auth/signup
```

```json
{
  "full_name": "Aarav Sharma",
  "email": "aarav@example.com",
  "password": "strongpass123",
  "role": "student",
  "department": "Computer Science",
  "semester": 5,
  "section": "CSE-A"
}
```

Login:

```http
POST /api/auth/login
```

Use the returned token on protected routes:

```http
Authorization: Bearer <access_token>
```

Profile:

```http
GET /api/auth/profile
```

Roles:

- `student`
- `teacher`
- `admin`

## API Response Format

Success:

```json
{
  "success": true,
  "message": "Human readable message",
  "data": {}
}
```

Error:

```json
{
  "success": false,
  "message": "Error message"
}
```

## Core APIs

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/timetable` | Get all timetable entries |
| GET | `/api/timetable/{day}` | Get timetable entries by day |
| POST | `/api/timetable` | Create timetable entry |
| DELETE | `/api/timetable/{id}` | Delete timetable entry |
| GET | `/api/events` | Get all events |
| POST | `/api/events` | Create event |
| DELETE | `/api/events/{id}` | Delete event |
| GET | `/api/notices` | Get all notices |
| POST | `/api/notices` | Create notice |
| GET | `/api/teachers` | Get all teachers |
| GET | `/api/teachers/{department}` | Get teachers by department |
| POST | `/api/teachers` | Create teacher |
| GET | `/api/clubs` | Get all clubs |
| POST | `/api/clubs` | Create club |

## Personalized APIs

Protected with JWT:

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/dashboard/me` | Aggregated dashboard for current user |
| GET | `/api/timetable/me` | Timetable filtered by section, department, semester |
| GET | `/api/notices/me` | Global and targeted notices |
| POST | `/api/events/bookmark/{id}` | Bookmark an event |
| DELETE | `/api/events/bookmark/{id}` | Remove event bookmark |
| GET | `/api/preferences` | Get user preferences |
| PUT | `/api/preferences` | Update user preferences |

## Admin APIs

Admin-only routes require a JWT for a user with role `admin`.

| Method | Endpoint |
| --- | --- |
| POST | `/api/admin/events` |
| PUT | `/api/admin/events/{id}` |
| DELETE | `/api/admin/events/{id}` |
| POST | `/api/admin/notices` |
| PUT | `/api/admin/notices/{id}` |
| POST | `/api/admin/timetable` |
| PUT | `/api/admin/timetable/{id}` |
| POST | `/api/admin/teachers` |
| PUT | `/api/admin/teachers/{id}` |
| POST | `/api/admin/clubs` |
| PUT | `/api/admin/clubs/{id}` |
| GET | `/api/admin/users` |
| POST | `/api/admin/attendance` |
| GET | `/api/admin/analytics` |

## Advanced APIs

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/search?q=` | Global regex-backed search across dashboard data |
| GET | `/api/notifications` | Current user's notifications |
| PUT | `/api/notifications/{id}/read` | Mark notification as read |
| GET | `/api/attendance/me` | Current user's attendance |
| GET | `/api/bus-routes` | List bus routes |
| GET | `/api/bus-routes/{id}` | Get bus route detail |

## Development Workflow

- Add request/response models in `app/schemas`.
- Keep route handlers thin in `app/routes`.
- Put all MongoDB operations in `app/services`.
- Use `app/dependencies/auth.py` for protected and role-protected routes.
- Use `app/security` for password and token logic.
- Use `app/utils/response.py` for consistent responses.
- Update indexes in `app/config/indexes.py` when adding new query patterns.

## Testing Workflow

Current verification is import and route-map based:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -c "import app.main; app.main.app.openapi(); print('import ok')"
```

For integration testing, run the server with a valid `.env`, create a user through signup, login, then call protected routes with the returned bearer token.
