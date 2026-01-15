# Z‑Vuln‑Lab — Privilege Escalation (Medium)

This lab simulates a realistic local privilege escalation scenario.

## Scenario
You have obtained a low-privilege shell on the system.

Your goal is to escalate privileges and read:


### Build Up
```bash
docker build -t privesc .

docker run -p 2222:22 --name lab privesc
```