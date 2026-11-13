# Middleware Header Bypass / RCE Lab

This lab demonstrates a trust-boundary failure: the PHP application treats a client-controlled `X-Middleware-Subrequest` header as proof that an internal middleware already authenticated the request. The bypass reaches an intentionally unsafe command-execution endpoint.

> Run this lab only on localhost or an isolated training network. The endpoint executes commands in the container.

## Run it

Requirements: Docker with Compose.

```bash
docker compose up --build
```

Open <http://localhost:8080>. To run the PoC from the repository root in another terminal:

```bash
python3 exploit/exp.py id
```

The normal dashboard credentials are `admin` / `Super3cret!Passw0rD`, but the PoC demonstrates that the forged header bypasses the session check. The lab's SUID binary is at `/usr/local/bin/checksys`; inspect its `PATH` handling after obtaining command execution.

Stop the lab with:

```bash
docker compose down
```

## What to study

Internal headers must be added and protected by a trusted proxy, not accepted from the public request. Authorization should be explicit, and command execution should not be exposed through a web parameter. The weak checks and command execution here are intentional.
