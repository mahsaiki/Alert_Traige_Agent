# Dockerfile for FastAPI backend
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./scripts ./scripts
COPY .env.example .env.example

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 