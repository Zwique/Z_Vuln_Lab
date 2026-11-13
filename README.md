# Container Privilege Escalation Lab

This lab gives you an SSH shell as a low-privilege `player` user inside a container. Your goal is to enumerate the services, review the internal backup service, exploit its command-injection flaw, and read the root flag.

> Run this lab only on localhost or an isolated training network. The container intentionally runs a vulnerable service as root.

## Run it

Requirements: Docker with Compose.

```bash
docker compose up --build -d
ssh player@127.0.0.1 -p 2222
```

The SSH password is `player`. If you reuse the port and see a host-key warning, remove only this lab's key:

```bash
ssh-keygen -R "[127.0.0.1]:2222"
```

The objectives are:

1. Read `/home/player/user.txt`.
2. Escalate to root through the intentionally vulnerable internal backup service.
3. Read `/root/root.txt`.

The complete walkthrough is in [WalkThrough.md](WalkThrough.md). Stop the lab with:

```bash
docker compose down
```

## What to study

The exercise combines service enumeration, SSH port forwarding, source review, command injection, and excessive service privileges. The blacklist checks in the backup service are intentionally incomplete; the walkthrough explains why allowlists and argument arrays are safer.
