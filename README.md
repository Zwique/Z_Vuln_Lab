# 🧪 Intentionally Vulnerable Web Lab (Beginner Friendly)

This project is a **deliberately vulnerable PHP web application** created for **beginners** to learn web exploitation in a **safe, local environment**.

It is ideal for:
- ✅ Web security beginners  
- ✅ CTF-style practice   
- ✅ Learning how vulnerabilities chain together in real applications  

> ⚠️ **WARNING**  
> This application is intentionally insecure.  
> **Never deploy it on the internet or in a production environment.** 

---

## 🎯 Learning Goal

Learn how small security bugs can escalate into critical impact by chaining vulnerabilities:


---

## 🛠️ Tech Stack

- PHP 7.4
- MariaDB 10.6
- Docker & Docker Compose
- Simple HTML / JavaScript frontend

---

## 🔥 Vulnerabilities Included

### ✅ SQL Injection (Beginner Friendly)

User input is directly embedded into SQL queries without sanitization:

```php
SELECT content FROM notes WHERE title = '$title'
```

This allows SQL injection, for example:
```
' UNION SELECT '{{whoami}}' --
```

The injected value is later processed by the template engine, leading to further exploitation.


This version:
- ✅ Fixes formatting
- ✅ Clearly explains **why** the payload matters
- ✅ Keeps it beginner-friendly
- ✅ Prepares readers for the SSTI → RCE step

---

## 🚀 Running the Lab (Docker)

This lab is fully Dockerized and runs locally.

### Build and Start

From the project root, run:

```bash
docker-compose build
docker-compose up
```
The application will be available at:
```
http://localhost:8080
```
To Stop the lab: 

```
docker-compose down
```

🧨 Exploit Script

A ready‑to‑use exploit script is provided for learning purposes:
```
/exploit/exp.py
```
Example usage:
```
python3 exploit/exp.py "id"
python3 exploit/exp.py "ls -la"
```

> [!NOTE]
> After gaining `www-data`, there is a privilege escalation vulnerability. Escalate to the `root` user and retrieve `flag.txt` from the /root directory.
