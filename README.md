# 🧪 Intentionally Vulnerable Web Lab — Version 2.0

A deliberately vulnerable PHP web application designed for beginners to learn modern web exploitation techniques in a safe, local environment.

<<<<<<< Updated upstream
It is ideal for:
- ✅ Web security beginners  
- ✅ CTF-style practice   
- ✅ Learning how vulnerabilities chain together in real applications  
=======
This version focuses on logic flaws and trust boundary violations inspired by real-world vulnerabilities and Hack The Box challenges.
>>>>>>> Stashed changes

> ⚠️ WARNING  
> This application is intentionally insecure.  
<<<<<<< Updated upstream
> **Never deploy it on the internet or in a production environment.** 
=======
> Never deploy it to the internet or production systems.
>>>>>>> Stashed changes

---

## 🎯 Learning Objectives

This lab demonstrates:

- How logic flaws can be more dangerous than injections
- Why trusting client-controlled headers is dangerous
- How authentication bypass leads to full system compromise
- Web → OS → root privilege escalation chains

---

## 🛠️ Tech Stack

- PHP 7.4 (Apache)
- MariaDB
- Docker & Docker Compose
- Linux privilege escalation (sudo misconfiguration)

---

## 🧩 Vulnerabilities Overview (v2.0)

### 🔥 X-Middleware-Subrequest Authentication Bypass

The application protects an admin endpoint using a middleware-style authorization check.  
However, it incorrectly trusts a client-supplied HTTP header:

X-Middleware-Subrequest


### Vulnerable Code

```php
function middleware_allows_access(): bool {
    $hdr = $_SERVER['HTTP_X_MIDDLEWARE_SUBREQUEST'] ?? '';

    // ❌ Vulnerable: trust client-controlled internal header
    if (strpos($hdr, 'middleware') !== false) {
        return true;
    }

    return isset($_SESSION['user']);
}
```

Why this is vulnerable

HTTP headers are fully attacker-controlled

The application trusts an internal-only header

Substring matching is used instead of strict validation

Any value containing middleware bypasses authentication

Example Bypass Header
```php
X-Middleware-Subrequest: middleware:middleware:middleware
```

🧨 Impact

1. An attacker can:

2. Bypass authentication

3. Access an admin-only endpoint

4. Execute system commands as www-data

5. Abuse a sudo misconfiguration

6. Escalate privileges to root

7. Read /root/flag.txt

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
