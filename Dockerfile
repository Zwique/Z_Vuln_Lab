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
    python3-pip \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask

RUN useradd -m -d /home/player -s /bin/bash player && \
    echo "player:player" | chpasswd

RUN useradd -m -d /home/git -s /bin/bash git

RUN mkdir /var/run/sshd && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Gitea binary (multi-arch support)
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ]; then \
        GITEA_ARCH="linux-arm64"; \
    elif [ "$ARCH" = "amd64" ]; then \
        GITEA_ARCH="linux-amd64"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    curl -L https://dl.gitea.com/gitea/1.21.0/gitea-1.21.0-${GITEA_ARCH} \
    -o /usr/local/bin/gitea && \
    chmod +x /usr/local/bin/gitea


RUN mkdir -p \
    /var/lib/gitea \
    /var/lib/gitea/custom \
    /var/lib/gitea/data \
    /var/lib/gitea/log \
    /var/lib/gitea/repositories \
    /etc/gitea && \
    chown -R git:git /var/lib/gitea /etc/gitea && \
    mkdir -p /data/git/.ssh && \
    chown -R git:git /data/git/.ssh


COPY app.ini /etc/gitea/app.ini
RUN chown git:git /etc/gitea/app.ini

COPY backend /opt/backend
RUN chown -R git:git /opt/backend


COPY init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY root.txt /root/root.txt
RUN chmod 600 /root/root.txt


COPY user.txt /home/player/user.txt
RUN chmod 644 /home/player/user.txt

RUN echo "Hint: Check running services and internal network ports" > /home/player/README.txt && \
    chown player:player /home/player/README.txt

EXPOSE 22

CMD ["/usr/bin/supervisord"]

