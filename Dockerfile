FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3 python3-pip sudo openssh-server \
    && mkdir /var/run/sshd

COPY backend/ /app/
COPY init.sh /init.sh
COPY user.txt /home/player/user.txt
COPY root.txt /root/root.txt

RUN chmod +x /init.sh && /init.sh && pip3 install -r /app/requirements.txt

EXPOSE 22 5000

CMD service ssh start && python3 /app/app.py
