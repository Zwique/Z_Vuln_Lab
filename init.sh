#!/bin/bash
set -e

sleep 6

echo "[+] Waiting for Gitea..."
until curl -s http://127.0.0.1:3000 > /dev/null; do
  sleep 1
done

echo "[+] Creating admin user..."

sudo -u git /usr/local/bin/gitea admin user create \
  --username dev \
  --password dev123 \
  --email dev@internal.local \
  --admin \
  --config /etc/gitea/app.ini || true

echo "[+] Creating backend repo..."

sudo -u git /usr/local/bin/gitea admin repo create \
  --owner dev \
  --name backend \
  --private=false \
  --config /etc/gitea/app.ini || true

echo "[+] Seeding vulnerable backend code..."

cd /opt/backend

if [ ! -d ".git" ]; then
  git init
  git config user.email "dev@internal.local"
  git config user.name "dev"
  git add .
  git commit -m "Initial vulnerable backend service"
fi

git branch -M main

git remote remove origin 2>/dev/null || true
git remote add origin http://dev:dev123@127.0.0.1:3000/dev/backend.git

git push -u origin main --force

echo "[+] Gitea seeding complete."
