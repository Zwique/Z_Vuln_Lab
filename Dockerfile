FROM python:3.11-slim

WORKDIR /app
COPY backend/ /app/
COPY flag.txt /app/flag.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9000
CMD ["python", "app.py"]
