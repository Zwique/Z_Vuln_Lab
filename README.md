# Z-Vuln-Lab v5.0 — JWT & OAuth Auth Bypass

This lab simulates modern authentication vulnerabilities involving JWT misuse and OAuth identity trust flaws.

## Objectives
Find and read:
- /home/player/user.txt
- /root/root.txt

## Setup
```bash
docker build -t jwt-oauth-lab .
docker run -d -p 2222:22 -p 5000:5000 --name jwtlab jwt-oauth-lab
ssh player@localhost -p 2222
password: player
