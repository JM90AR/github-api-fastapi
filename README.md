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
| Railway | Cloud deployment |

---

## 📌 Features

- 🔐 **API Key Authentication** — All endpoints are protected. Requests without a valid API key are rejected with a `401 Unauthorized` response.
- ✅ **Pydantic Models** — Every response has a strictly defined schema, ensuring consistent and validated data output.
- 🚦 **Rate Limiting** — Maximum 10 requests per minute per client. Exceeding the limit returns a `429 Too Many Requests` error.
- ❌ **Error Handling** — If a GitHub user doesn't exist, the API returns a clear `404 Not Found` response instead of crashing.
- 🗄️ **Query History** — Every API call is logged to a PostgreSQL database with the username and timestamp.
- 📄 **Auto-generated Docs** — FastAPI automatically generates interactive API documentation at `/docs`.
- ☁️ **Cloud Deployment** — Deployed on Railway with PostgreSQL as a managed database service.

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
Headers: X-API-Key: your-api-key
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

### Run locally with Docker (recommended)

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

4. Authenticate using the **Authorize** button with your API key.

---

## ☁️ Deploy on Railway

This project is configured to deploy on [Railway](https://railway.app) with a managed PostgreSQL database.

### Steps to deploy:

1. Create an account on [railway.app](https://railway.app) and login with GitHub
2. Click **New Project** → **Deploy from GitHub repo** → select this repo
3. Add a **PostgreSQL** database service to the project
4. Go to your API service → **Variables** → add:
   - `DB_URL` = your PostgreSQL connection URL from Railway
5. Railway will automatically build and deploy using the Dockerfile
6. Go to **Settings** → **Networking** → **Generate Domain** to get a public URL
7. Access your live API at:
```
https://your-project.up.railway.app/docs
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DB_URL` | PostgreSQL connection URL |

---

## 📁 Project Structure

```
github-api-fastapi/
├── main.py              # FastAPI application
├── Dockerfile           # Container definition
├── docker-compose.yml   # Multi-container local setup
└── requirements.txt     # Python dependencies
```

---

## 📫 Contact

Created by **Miguel Alba**  
Feel free to connect or reach out!
