FROM python:latest
WORKDIR /app
COPY . .
# rebuild v2
RUN pip install fastapi uvicorn requests psycopg2-binary
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]