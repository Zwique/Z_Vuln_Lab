# Intentional Remote Code Execution Training Machine SSTI (Version 1.0)

This project provides a deliberately vulnerable environment designed for security research, exploit development practice, and CTF‑style challenges.  
Instead, it demonstrates a similar severity class vulnerability using a custom, insecure PHP backend.

---

## Vulnerability Summary

The main vulnerability is a **Remote Code Execution (RCE)** flaw caused by an intentionally unsafe template engine.

### Vulnerable Functions

```php
dangerous_template_render()
dangerous_exec()
shell_exec()
```

User-controlled template expressions inside {{ ... }} are executed directly on the server:
```{{ id }}```
This becomes:
```
shell_exec("id");
```

# Features of This Lab

- PHP 7.4 backend with intentionally insecure code

- Custom template engine supporting full RCE

- LFI vulnerability in `render.php?page=`

- Weak login system

- Unsafe file upload endpoint

- Supports:

    - Local File Inclusion (LFI)

    - Remote Code Execution (RCE)

- Simple HTML/JS frontend

- Dockerized for easy deployment
- 
> [!NOTE]
> PHP 7.4 backend with intentionally insecure code

🚀 Running the Machine

Build and start:

```docker-compose build
docker-compose up
```


## Access at:

http://localhost:8080/

🧪 Exploitation Examples
RCE (Template Injection)
```POST /api/render.php
page={{ id }}
```
LFI (Read System Files)
```
GET /api/render.php?page=../../../../etc/passwd
```
### Using the Provided PoC Script
```
python3 exp.py lfi /etc/passwd
python3 exp.py rce "id"
```
### PoC
<img width="1048" height="541" alt="example" src="https://github.com/user-attachments/assets/4f245f97-70dd-45e8-b0c6-c7b81b2db2e7" />
