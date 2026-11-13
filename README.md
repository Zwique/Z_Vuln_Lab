# JWT Authentication Bypass Lab

This lab demonstrates an intentionally unsafe JWT verification decision: the application decodes the token without verifying its signature. A learner can change the `role` claim to `admin` and access the protected flag.

> Run this lab only on localhost or an isolated training network.

## Run it

Requirements: Docker with Compose.

```bash
docker compose up --build
```

Open <http://localhost:9000>. The normal login is:

```text
Username: player
Password: player
```

To demonstrate the bypass from another terminal:

```bash
python3 exploit/exp.py
```

The script creates an unsigned JWT with `role=admin` and requests `/admin`. Use `--url http://HOST:9000` when the lab is running on another host.

Stop the lab with:

```bash
docker compose down
```

## What to study

JWTs are encoded, not encrypted. Decoding a token is fine for inspection, but authorization must use a verified signature, an allow-listed algorithm, and validated claims. The broken verification is intentional for this exercise; do not copy it into a real application.
