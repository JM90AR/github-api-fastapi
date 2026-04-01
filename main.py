from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Optional
import requests
import psycopg2
from datetime import datetime
from collections import defaultdict
import time
import os

app = FastAPI(title="GitHub API", description="API para consultar perfiles de GitHub")

BASE_URL = "https://api.github.com/users"
API_KEY = "mi-clave-secreta-123"
api_key_header = APIKeyHeader(name="X-API-Key")

# Rate limiting
request_counts = defaultdict(list)
MAX_REQUESTS = 10
WINDOW_SECONDS = 60

# Modelos Pydantic
class PerfilResponse(BaseModel):
    nombre: Optional[str]
    bio: Optional[str]
    repos: int
    seguidores: int

class RepoResponse(BaseModel):
    nombre: str
    descripcion: Optional[str]
    lenguaje: Optional[str]

class ConsultaResponse(BaseModel):
    usuario: str
    fecha: str

# Funciones
def verificar_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida")
    return key

def verificar_rate_limit(request: Request):
    ip = request.client.host
    ahora = time.time()
    request_counts[ip] = [t for t in request_counts[ip] if ahora - t < WINDOW_SECONDS]
    if len(request_counts[ip]) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Demasiadas peticiones, espera un minuto")
    request_counts[ip].append(ahora)

def get_db():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL no está configurada")
    return psycopg2.connect(database_url)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(100),
            fecha TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def registrar(usuario):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO consultas (usuario, fecha) VALUES (%s, %s)",
                (usuario, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()

@app.get("/")
def inicio():
    return {"mensaje": "API de GitHub con FastAPI"}

@app.get("/perfil/{usuario}", response_model=PerfilResponse)
def perfil(usuario: str, request: Request, key: str = Security(api_key_header)):
    verificar_key(key)
    verificar_rate_limit(request)
    registrar(usuario)
    data = requests.get(f"{BASE_URL}/{usuario}").json()
    if "message" in data and data["message"] == "Not Found":
        raise HTTPException(status_code=404, detail=f"Usuario '{usuario}' no existe en GitHub")
    return PerfilResponse(
        nombre=data["name"],
        bio=data["bio"],
        repos=data["public_repos"],
        seguidores=data["followers"]
    )

@app.get("/repos/{usuario}", response_model=list[RepoResponse])
def repos(usuario: str, request: Request, key: str = Security(api_key_header)):
    verificar_key(key)
    verificar_rate_limit(request)
    registrar(usuario)
    data = requests.get(f"{BASE_URL}/{usuario}").json()
    if "message" in data and data["message"] == "Not Found":
        raise HTTPException(status_code=404, detail=f"Usuario '{usuario}' no existe en GitHub")
    repos_data = requests.get(f"{BASE_URL}/{usuario}/repos").json()
    return [RepoResponse(
        nombre=r["name"],
        descripcion=r["description"],
        lenguaje=r["language"]
    ) for r in repos_data]

@app.get("/historial", response_model=list[ConsultaResponse])
def historial(key: str = Security(api_key_header)):
    verificar_key(key)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT usuario, fecha FROM consultas ORDER BY fecha DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [ConsultaResponse(usuario=r[0], fecha=str(r[1])) for r in rows]

@app.on_event("startup")
def startup():
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'NO ENCONTRADA')}")
    init_db()