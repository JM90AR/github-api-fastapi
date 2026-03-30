# GitHub API - FastAPI 🚀

A production-ready REST API built with **Python**, **FastAPI**, **PostgreSQL**, and **Docker** that queries real-time data from the GitHub API. This project demonstrates modern backend development practices including authentication, data validation, rate limiting, and containerization.

---

## 🔧 Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3 | Core language |
| FastAPI | Web framework |
| PostgreSQL | Database for query history |
| Pydantic | Data validation and response models |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Uvicorn | ASGI server |

---

## 📌 Features

- 🔐 **API Key Authentication** — All endpoints are protected. Requests without a valid API key are rejected with a `401 Unauthorized` response.
- ✅ **Pydantic Models** — Every response has a strictly defined schema, ensuring consistent and validated data output.
- 🚦 **Rate Limiting** — Maximum 10 requests per minute per client. Exceeding the limit returns a `429 Too Many Requests` error.
- ❌ **Error Handling** — If a GitHub user doesn't exist, the API returns a clear `404 Not Found` response instead of crashing.
- 🗄️ **Query History** — Every API call is logged to a PostgreSQL database with the username and timestamp.
- 📄 **Auto-generated Docs** — FastAPI automatically generates interactive API documentation at `/docs`.

---

## 🗂 API Endpoints

| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| GET | `/` | Health check | ❌ |
| GET | `/perfil/{usuario}` | Get GitHub user profile | ✅ |
| GET | `/repos/{usuario}` | List user's repositories | ✅ |
| GET | `/historial` | View last 10 queries from DB | ✅ |

---

## 🧠 How It Works

```
Client Request
      ↓
API Key Verification → 401 if invalid
      ↓
Rate Limit Check → 429 if exceeded
      ↓
GitHub API Call → 404 if user not found
      ↓
Save to PostgreSQL
      ↓
Return validated JSON (Pydantic)
```

---

## 🗂 Example Usage

### Get a user profile

**Request:**
```
GET /perfil/torvalds
Headers: X-API-Key: mi-clave-secreta-123
```

**Response:**
```json
{
  "nombre": "Linus Torvalds",
  "bio": null,
  "repos": 11,
  "seguidores": 292100
}
```

### User not found

**Request:**
```
GET /perfil/usuarioquenoeexiste
Headers: X-API-Key: mi-clave-secreta-123
```

**Response:**
```json
{
  "detail": "Usuario 'usuarioquenoeexiste' no existe en GitHub"
}
```

### Rate limit exceeded

```json
{
  "detail": "Demasiadas peticiones, espera un minuto"
}
```

---

## ⚙️ Setup Instructions

### Requirements

- Docker
- Docker Compose

### Run with Docker (recommended)

1. Clone this repository:
```bash
git clone https://github.com/JM90AR/github-api-fastapi.git
cd github-api-fastapi
```

2. Build and start all containers:
```bash
docker compose up --build
```

3. Open the interactive API docs:
```
http://localhost:8000/docs
```

4. Authenticate using the **Authorize** button with the API key:
```
mi-clave-secreta-123
```

### Run without Docker

1. Install dependencies:
```bash
pip install fastapi uvicorn requests psycopg2-binary
```

2. Set up a PostgreSQL database and update the connection settings in `main.py`.

3. Run the server:
```bash
uvicorn main:app --reload
```

---

## 📁 Project Structure

```
github-api-fastapi/
├── main.py              # FastAPI application
├── Dockerfile           # Container definition
├── docker-compose.yml   # Multi-container setup
└── requirements.txt     # Python dependencies
```

---

## 📫 Contact

Created by **Miguel Alba**  
Feel free to connect or reach out!
