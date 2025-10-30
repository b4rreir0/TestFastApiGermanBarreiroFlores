FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV DATABASE_URL=postgresql+asyncpg://postgres:1234@db:5432/fastapi_challenge
ENV SECRET_KEY=12345678abcdefghijklmnop
ENV ALGORITHM=HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES=60

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]