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

echo "[+] Preparing backend code..."
cd /opt/backend

# Initialize git repo
rm -rf .git
sudo -u git git init
sudo -u git git config user.email "dev@internal.local"
sudo -u git git config user.name "dev"
sudo -u git git add .
sudo -u git git commit -m "Initial vulnerable backend service"
sudo -u git git branch -M main

echo "[+] Creating repository via API..."
# Create repository using Gitea API
curl -X POST "http://127.0.0.1:3000/api/v1/user/repos" \
  -u "dev:dev123" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "backend",
    "description": "Internal Backend Service",
    "private": false,
    "auto_init": false,
    "default_branch": "main"
  }' || true

sleep 2

echo "[+] Pushing code to repository..."
# Push to the repository
sudo -u git git remote add origin http://dev:dev123@127.0.0.1:3000/dev/backend.git
sudo -u git git push -u origin main --force

echo "[+] Gitea seeding complete."