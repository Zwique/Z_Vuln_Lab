#!/bin/bash

useradd -m player
echo "player:player" | chpasswd

COPY user.txt /home/player/user.txt
chmod 644 /home/player/user.txt
chown player:player /home/player/user.txt

COPY root.txt /root/root.txt
chmod 600 /root/root.txt


cat > /opt/backup.py << 'EOF'
import os
os.system("tar -czf /tmp/backup.tar.gz /home/player")
EOF

chmod 755 /opt/backup.py

echo "player ALL=(root) NOPASSWD: /usr/bin/python3 /opt/backup.py" >> /etc/sudoers
