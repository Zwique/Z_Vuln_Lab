# Z‑Vuln‑Lab — Privilege Escalation (Medium)

This lab simulates a realistic local privilege escalation scenario within a containerized environment.

## Scenario
You have obtained a low-privilege shell on the system. Your goal is to identify misconfigurations or vulnerabilities to escalate your privileges to `root`.

### Objectives
Find and read the following flags:
1. `/home/player/user.txt`
2. `/root/root.txt`

---

## Setup Instructions

### 1. Build & Run
Execute the following commands to build the image and start the lab:

```bash
# Build the Docker image
docker build -t privesc .

# Start the container
docker run -d -p 2222:22 --name lab privesc
```

2. Access the System
Log in as the user player using the password player.

`player:player`


```bash
➜  SSTI_Vuln git:(privesc-only) ✗ ssh player@localhost -p 2222
player@localhost's password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.12.54-linuxkit aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Mon Jan 19 21:15:20 2026 from 192.168.65.1
player@4ab7cc9b6fb8:~$ whoami
player
player@4ab7cc9b6fb8:~$ 
```

> [!WARNING]
> If you see something `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`, use `ssh-keygen -R "[localhost]:2222"` command to remove old host keys.

> [!IMPORTANT]
> This lab uses binaries compiled for ARM64. If you are on an x86_64 Windows/Linux machine, please use the compatible x86 version here.

WalkThrough:

Check out the <a href="WalkThrough.md">WalkThrough.md</a> if you're stuck.