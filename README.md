# 🔥 Z-Vuln-Lab — HTTP Request Smuggling Challenge

This lab demonstrates a real-world **HTTP Request Smuggling** vulnerability caused by inconsistent request parsing between frontend and backend servers.

Participants must exploit this parsing mismatch to smuggle a hidden request and access a protected admin endpoint.

---

## 🧠 Vulnerability Overview

**HTTP Request Smuggling** occurs when:

- A frontend server parses requests using **Content-Length**, and
- A backend server parses requests using **Transfer-Encoding: chunked**,

allowing attackers to craft a single request that is interpreted as **two separate requests** by different servers.

## 📁 Project Structure

Each lab exists in a separate branch:

- 🔐 **JWT Auth Bypass (OAuth)**  
  Branch: `jwt-oauth`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/jwt-oauth

- 🧗 **Privilege Escalation**  
  Branch: `privesc-v3`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/privesc-v3

- 🧱 **Middleware Vulnerabilities**  
  Branch: `middleware-v2`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/middleware-v2

- 🧬 **Server-Side Template Injection (SSTI)**  
  Branch: `ssti-v1`  
  https://github.com/Zwique/Z_Vuln_Lab/tree/ssti-v1

---

## 🏷️ Tags & Releases

- 🔐 **v4.0-jwt-oauth**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v4.0-jwt-oauth

- 🧗 **v3.0-privesc**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v3.0-privesc

- 🧱 **v2.0-middleware**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v2.0-middleware

- 🧬 **v1.0-ssti**  
  https://github.com/Zwique/Z_Vuln_Lab/releases/tag/v1.0-ssti

---

## 🚀 How to Use

```bash
git clone https://github.com/Zwique/Z_Vuln_Lab.git
cd Z_Vuln_Lab
git checkout jwt-oauth
