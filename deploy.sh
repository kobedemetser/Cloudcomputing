#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "==> Pulling latest images..."
docker compose pull

echo "==> Stopping old containers..."
docker compose down

echo "==> Building custom image and starting stack..."
docker compose up -d --build

echo "==> Stack is running. Services:"
docker compose ps
