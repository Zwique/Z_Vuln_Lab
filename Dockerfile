FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openssh-server \
    supervisor \
    sqlite3 \
    git \
    curl \
    ca-certificates \
    sudo \
    python3 \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# ---- Users ----
RUN useradd -m -d /home/player -s /bin/bash player && \
    echo "player:player" | chpasswd

RUN useradd -m -d /home/git -s /bin/bash git

# ---- SSH ----
RUN mkdir /var/run/sshd && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# ---- Gitea binary (ARM64) ----
RUN curl -L https://dl.gitea.com/gitea/1.21.0/gitea-1.21.0-linux-arm64 \
    -o /usr/local/bin/gitea && \
    chmod +x /usr/local/bin/gitea

# ---- Gitea layout (CRITICAL) ----
RUN mkdir -p \
    /var/lib/gitea \
    /var/lib/gitea/custom \
    /var/lib/gitea/data \
    /var/lib/gitea/log \
    /var/lib/gitea/repositories \
    /etc/gitea && \
    chown -R git:git /var/lib/gitea /etc/gitea

# ---- Config ----
COPY app.ini /etc/gitea/app.ini
RUN chown git:git /etc/gitea/app.ini

# ---- Supervisor ----
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ---- Flag ----
COPY flag.txt /root/flag.txt
RUN chmod 600 /root/flag.txt

EXPOSE 22

CMD ["/usr/bin/supervisord"]
