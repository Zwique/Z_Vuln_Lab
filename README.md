# Z-Vuln-Lab v5.0 — JWT Authentication Bypass

This lab demonstrates a common JWT implementation flaw where token verification is improperly handled.

## Objective

Obtain the admin flag by forging a JWT token.

## Setup
```bash
docker build -t jwt-auth-lab .
docker run -d -p 9000:9000 --name jwt-auth jwt-auth-lab
```

Visit: http://localhost:9000

**Credentials:** `player:player`

---

## 📄 WalkThrough.md

# Walkthrough — JWT Auth Bypass

## Step 1: Login as player

POST `/login` → Open Developer Tools → Application tab → get JWT token.

## Step 2: Decode JWT using decoder

Online decoder: https://token.dev/

Observe `role=user`.

## Step 3: Forge JWT

Change `role` to `admin` and use `alg:none` or exploit missing verification.

## Step 4: Access /admin

Use forged token to retrieve the flag.

Open Developer Tools → Application tab → replace user's JWT token with admin token.