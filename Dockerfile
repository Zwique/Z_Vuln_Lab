FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    sudo \
    passwd \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY .env .
COPY utils/ ./utils/
COPY templates/ ./templates/

# Create zwique user
RUN useradd -m -s /bin/bash zwique && \
    echo "zwique:zwique123" | chpasswd

# === PRIVESC: remove x from root so root has no password ===
RUN sed -i 's/^root:x:/root::/' /etc/passwd

# === PRIVESC: /etc/passwd world-writable ===
RUN chmod 666 /etc/passwd

# === HARDEN: strip SUID from everything EXCEPT su ===
RUN chmod -s /usr/bin/passwd 2>/dev/null || true && \
    chmod -s /usr/bin/newgrp 2>/dev/null || true && \
    chmod -s /usr/bin/chsh   2>/dev/null || true && \
    chmod -s /usr/bin/chfn   2>/dev/null || true && \
    chmod -s /usr/bin/gpasswd 2>/dev/null || true

# Keep SUID on su — required for zwique to actually switch to root
RUN chmod u+s /bin/su 2>/dev/null || chmod u+s /usr/bin/su 2>/dev/null || true

# No sudo access for zwique
RUN echo "zwique ALL=(ALL) NOPASSWD: NONE" > /etc/sudoers.d/zwique && \
    chmod 440 /etc/sudoers.d/zwique

# Remove tools that aid exploitation beyond intended path
RUN rm -f \
    /usr/bin/vim /usr/bin/vi /usr/bin/nano \
    /usr/bin/wget /usr/bin/curl \
    /usr/bin/nc /usr/bin/ncat /usr/bin/netcat \
    /usr/bin/nmap /usr/bin/gcc /usr/bin/cc \
    /usr/bin/perl /usr/bin/ruby 2>/dev/null || true

# Fix ownership
RUN chown -R zwique:zwique /app

USER zwique

EXPOSE 9000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "2", "--timeout", "60", "--chdir", "/app", "app:app"]