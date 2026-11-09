#!/usr/bin/env bash
# ============================================================
# SELF-HEALING - reinicia um Deployment com seguranca (Fase 4)
# ============================================================
# Chamado pelo workflow .github/workflows/self-healing.yml quando o
# alerta do Grafana dispara. Tambem roda a mao, com o kubectl ja
# apontado para o cluster:
#
#   SERVICE=flag-service bash scripts/self-healing/restart.sh
#
# O QUE ELE GARANTE, nesta ordem:
#   1. ALLOWLIST: so reinicia um dos 5 servicos da aplicacao. O nome vem
#      de fora (payload do alerta), entao e comparado por igualdade com
#      a lista - nunca usado como padrao ou expressao. Nome fora da lista
#      encerra com codigo 2, sem chamar o kubectl.
#   2. COOLDOWN: se o mesmo Deployment foi reiniciado ha menos de
#      COOLDOWN_SECONDS, nao reinicia de novo. Sem isso, um alerta que
#      oscila entre Firing e Normal reiniciaria o servico em laco. O
#      instante do ultimo reinicio vem da anotacao que o proprio
#      `kubectl rollout restart` grava no template do pod.
#   3. RESULTADO VERIFICAVEL: depois do restart, espera o rollout
#      terminar (`rollout status`) e falha se ele nao concluir no prazo.
#
# SAIDAS: codigo 0 quando reiniciou ou quando o cooldown impediu (as duas
# sao decisoes corretas); 1 em erro do kubectl ou rollout que nao
# terminou; 2 em servico recusado. No GitHub Actions, grava result=...
# em $GITHUB_OUTPUT e um resumo em $GITHUB_STEP_SUMMARY.
# ============================================================
set -euo pipefail

ALLOWLIST=(auth-service flag-service targeting-service evaluation-service analytics-service)

service="${SERVICE:-}"
# Status do alerta no payload do Grafana; disparo manual conta como firing.
alert_status="${ALERT_STATUS:-firing}"
namespace="${NAMESPACE:-togglemaster}"
cooldown="${COOLDOWN_SECONDS:-600}"
rollout_timeout="${ROLLOUT_TIMEOUT:-180s}"
kubectl_bin="${KUBECTL:-kubectl}"

# Escreve no resumo do job e no log, sempre a mesma frase.
report() {
  echo "$1"
  if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
    echo "$1" >> "$GITHUB_STEP_SUMMARY"
  fi
}

set_output() {
  if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
    echo "result=$1" >> "$GITHUB_OUTPUT"
  fi
}

# --- 0. so age sobre alerta em Firing -----------------------------------
# O contact point do GitHub nao envia a resolucao (disableResolveMessage),
# mas a conferencia aqui impede que uma mudanca futura naquele arquivo
# transforme "voltou ao normal" em um restart.
if [[ "$alert_status" != "firing" ]]; then
  if [[ "$alert_status" == "resolved" ]]; then
    report "Self-healing ignorado: o alerta ja foi resolvido."
  else
    report "Self-healing ignorado: status do alerta desconhecido."
  fi
  set_output ignored
  exit 0
fi

# --- 1. allowlist ------------------------------------------------------
allowed=false
for name in "${ALLOWLIST[@]}"; do
  if [[ "$service" == "$name" ]]; then
    allowed=true
    break
  fi
done
if [[ "$allowed" != true ]]; then
  # O valor recusado nao e repetido no log: pode ser texto arbitrario.
  report "Self-healing recusado: o servico pedido nao esta na allowlist (${ALLOWLIST[*]})."
  set_output refused
  exit 2
fi

if ! [[ "$cooldown" =~ ^[0-9]+$ ]]; then
  report "COOLDOWN_SECONDS precisa ser um numero inteiro de segundos."
  set_output refused
  exit 2
fi

# --- 2. cooldown ---------------------------------------------------------
# A anotacao fica vazia se o Deployment nunca foi reiniciado com o kubectl.
last_restart="$("$kubectl_bin" get deployment "$service" -n "$namespace" \
  -o 'jsonpath={.spec.template.metadata.annotations.kubectl\.kubernetes\.io/restartedAt}')"

if [[ -n "$last_restart" ]]; then
  last_epoch="$(date -u -d "$last_restart" +%s)"
  now_epoch="$(date -u +%s)"
  elapsed=$(( now_epoch - last_epoch ))
  if (( elapsed < cooldown )); then
    report "Self-healing ignorado: $service foi reiniciado ha ${elapsed}s (cooldown de ${cooldown}s, ultimo restart em $last_restart)."
    set_output cooldown
    exit 0
  fi
fi

# --- 3. restart e verificacao -------------------------------------------
report "Reiniciando deployment/$service no namespace $namespace."
"$kubectl_bin" rollout restart "deployment/$service" -n "$namespace"

if ! "$kubectl_bin" rollout status "deployment/$service" -n "$namespace" --timeout="$rollout_timeout"; then
  report "O rollout de $service nao terminou em $rollout_timeout."
  set_output failed
  exit 1
fi

report "Self-healing concluido: $service reiniciado e com o rollout completo."
set_output restarted
