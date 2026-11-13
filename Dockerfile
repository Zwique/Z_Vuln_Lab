FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    passwd \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY utils/ ./utils/
COPY templates/ ./templates/

ENV REDIS_HOST=redis \
    REDIS_PORT=6379

# Create the low-privilege lab user.
RUN useradd -m -s /bin/bash zwique && \
    echo "zwique:zwique123" | chpasswd

# Intentional privilege-escalation setup for the lab.
RUN sed -i 's/^root:x:/root::/' /etc/passwd && \
    chmod 666 /etc/passwd

# Keep SUID on su and remove it from unrelated helpers.
RUN chmod -s /usr/bin/passwd 2>/dev/null || true && \
    chmod -s /usr/bin/newgrp 2>/dev/null || true && \
    chmod -s /usr/bin/chsh 2>/dev/null || true && \
    chmod -s /usr/bin/chfn 2>/dev/null || true && \
    chmod -s /usr/bin/gpasswd 2>/dev/null || true && \
    chmod u+s /bin/su 2>/dev/null || chmod u+s /usr/bin/su 2>/dev/null || true

RUN echo "zwique ALL=(ALL) NOPASSWD: NONE" > /etc/sudoers.d/zwique && \
    chmod 440 /etc/sudoers.d/zwique

RUN rm -f \
    /usr/bin/vim /usr/bin/vi /usr/bin/nano \
    /usr/bin/wget /usr/bin/curl \
    /usr/bin/nc /usr/bin/ncat /usr/bin/netcat \
    /usr/bin/nmap /usr/bin/gcc /usr/bin/cc \
    /usr/bin/perl /usr/bin/ruby 2>/dev/null || true

RUN chown -R zwique:zwique /app

COPY flags/root.txt /root/root.txt
RUN chmod 600 /root/root.txt

COPY flags/user.txt /home/zwique/user.txt
RUN chmod 644 /home/zwique/user.txt

USER zwique

EXPOSE 9000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "2", "--timeout", "60", "--chdir", "/app", "app:app"]
