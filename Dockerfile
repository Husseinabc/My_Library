FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    sqlalchemy \
    "psycopg[binary]" \
    alembic \
    python-dotenv \
    "pwdlib[argon2]" \
    pyjwt \
    authlib\
    httpx\
    itsdangerous\
    python-multipart

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]