FROM python:latest
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn requests psycopg2-binary
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]