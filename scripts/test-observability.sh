#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Somente ambiente fictício. Mantém a sobreposição OTel nas recriações do teste.
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-tc04-integration}"
export COMPOSE_FILE="docker-compose.yaml:docker-compose.integration.yaml:docker-compose.otel.yaml"
export COMPOSE_PATH_SEPARATOR=:
export OTEL_TRACE_DIR="${OTEL_TRACE_DIR:-./00_COLAB_IA/02_TRABALHO/qa-otel}"
export OTEL_UID="${OTEL_UID:-$(id -u)}"
export OTEL_GID="${OTEL_GID:-$(id -g)}"
unset SERVICE_API_KEY
mkdir -p "$OTEL_TRACE_DIR"

docker compose --env-file .env.example config --quiet
# Git Bash deve preservar o caminho Linux passado ao processo do contêiner.
MSYS_NO_PATHCONV=1 docker compose --env-file .env.example run --rm --no-deps otel-collector validate --config=/etc/otelcol-contrib/config.yaml
docker compose --env-file .env.example up --build -d --wait --wait-timeout 240
python3 scripts/integration/test-flow.py
python3 scripts/integration/test-traces.py
