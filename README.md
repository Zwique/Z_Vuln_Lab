# Server-Side Template Injection Lab

This lab demonstrates an intentionally unsafe PHP template preview. A logged-in user can save PHP code as a template; the preview endpoint evaluates it on the server and returns the output. The branch also contains an intentionally unsafe command endpoint for comparison with the middleware lab.

> Run this lab only on localhost or an isolated training network. The template and admin endpoints execute code in the container.

## Run it

Requirements: Docker with Compose.

```bash
docker compose up --build
```

Open <http://localhost:8080> and log in with:

```text
Username: admin
Password: Super3cret!Passw0rD
```

From another terminal, save and render a simple command-execution template with the included PoC:

```bash
python3 exploit/ssti.py
```

Or use the dashboard manually. Enter this template, save it, and select **Render Template**:

```php
<?php system('id'); ?>
```

The root flag is at `/root/flag.txt` after the intended `www-data` to root exercise. Stop the lab with:

```bash
docker compose down
```

The branch also includes a separate middleware-header exercise:

```bash
python3 exploit/exp.py id
```

## What to study

Template engines should treat user input as data and should never pass it to PHP `eval()`. The application, SUID helper, and command endpoint are deliberately unsafe for training; do not deploy this branch as a real service.
