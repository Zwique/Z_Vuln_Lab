# 🧪 Z-Vuln-Lab — Vulnerability Practice Labs

Z-Vuln-Lab is a hands-on web security lab series designed to help learners practice real-world vulnerabilities such as authentication bypass, SSTI, privilege escalation, and middleware flaws. Each vulnerability is isolated into its own Git branch.

---

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

## 🏷️ Tags & Stable Releases

Some branches are tagged to mark stable lab versions, for example:

- `v4.0-jwt-oauth` — Stable release of the JWT OAuth bypass lab

Tags allow you to reference exact versions for teaching, write-ups, or competitions.

---

## 🚀 How to Use

```bash
git clone https://github.com/Zwique/Z-Vuln-Lab.git
cd Z-Vuln-Lab
git checkout jwt-oauth
