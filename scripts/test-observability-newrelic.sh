#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Mesmo ensaio do test-observability.sh, com os traces também exportados ao New Relic.
# Requer NEW_RELIC_LICENSE_KEY no .env local (ignorado pelo Git). No Windows: PYTHON="py -3".
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-tc04-integration}"
export COMPOSE_FILE="docker-compose.yaml:docker-compose.integration.yaml:docker-compose.otel.yaml:docker-compose.newrelic.yaml"
export COMPOSE_PATH_SEPARATOR=:
export OTEL_TRACE_DIR="${OTEL_TRACE_DIR:-./00_COLAB_IA/02_TRABALHO/qa-otel-newrelic}"
export OTEL_UID="${OTEL_UID:-$(id -u)}"
export OTEL_GID="${OTEL_GID:-$(id -g)}"
PYTHON="${PYTHON:-python3}"
unset SERVICE_API_KEY
mkdir -p "$OTEL_TRACE_DIR"

grep -q '^NEW_RELIC_LICENSE_KEY=.' .env 2>/dev/null || { echo "Defina NEW_RELIC_LICENSE_KEY no .env local." >&2; exit 1; }
# Os testes Python chamam o Compose só com o .env.example; exportar a chave (e apenas ela)
# deixa a interpolação do overlay funcionar nesses comandos também.
NEW_RELIC_LICENSE_KEY="$(grep -E '^NEW_RELIC_LICENSE_KEY=' .env | head -1 | cut -d= -f2-)"
export NEW_RELIC_LICENSE_KEY
# O exemplo traz os valores fictícios dos serviços; o .env local acrescenta só a chave.
ENV_FILES=(--env-file .env.example --env-file .env)

docker compose "${ENV_FILES[@]}" config --quiet
# Git Bash deve preservar o caminho Linux passado ao processo do contêiner.
MSYS_NO_PATHCONV=1 docker compose "${ENV_FILES[@]}" run --rm --no-deps otel-collector validate \
  --config=/etc/otelcol-contrib/config.yaml --config=/etc/otelcol-contrib/newrelic.yaml
docker compose "${ENV_FILES[@]}" up --build -d --wait --wait-timeout 240
$PYTHON scripts/integration/test-flow.py
$PYTHON scripts/integration/test-traces.py

# Espera o último lote sair e procura só falhas de exportação; a chave nunca é impressa.
sleep 15
if docker compose "${ENV_FILES[@]}" logs otel-collector 2>&1 | grep -iE 'exporting failed|permanent error|forbidden|unauthorized'; then
  echo "Falha na exportação ao New Relic: confira a chave (Ingest - License) e a região US." >&2
  exit 1
fi
echo "Exportação sem erros no Collector. No New Relic: APM & Services > Services - OpenTelemetry, Service map e Distributed tracing."
