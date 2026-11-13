FROM python:3.12-slim

WORKDIR /app

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY exp.py ./exp.py

EXPOSE 8000

CMD ["python", "backend/vulnerable_backend.py"]
