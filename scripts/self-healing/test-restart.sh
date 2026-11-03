#!/usr/bin/env bash
# Testes do restart.sh sem cluster: um kubectl falso registra as chamadas
# e devolve a anotacao restartedAt que cada cenario precisa.
#   bash scripts/self-healing/test-restart.sh
set -euo pipefail
cd "$(dirname "$0")"

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

cat > "$work/kubectl" <<'FAKE'
#!/usr/bin/env bash
echo "$*" >> "$FAKE_LOG"
case "$1 $2" in
  "get deployment") printf '%s' "${FAKE_RESTARTED_AT:-}" ;;
  "rollout restart") echo "deployment.apps/$3 restarted" ;;
  "rollout status") exit "${FAKE_STATUS_EXIT:-0}" ;;
esac
FAKE
chmod +x "$work/kubectl"

failures=0
iso_ago() { date -u -d "@$(( $(date -u +%s) - $1 ))" +%Y-%m-%dT%H:%M:%SZ; }

# run <nome> <codigo esperado> <result esperado> <restart esperado: sim|nao> [VAR=valor...]
run() {
  local name="$1" want_code="$2" want_result="$3" want_restart="$4"
  shift 4
  : > "$work/log"
  : > "$work/output"
  local code=0
  env FAKE_LOG="$work/log" KUBECTL="$work/kubectl" GITHUB_OUTPUT="$work/output" \
    GITHUB_STEP_SUMMARY="$work/summary" "$@" bash ./restart.sh > "$work/stdout" 2>&1 || code=$?
  local result restarted=nao
  result="$(sed -n 's/^result=//p' "$work/output")"
  grep -q "^rollout restart" "$work/log" && restarted=sim
  if [[ "$code" == "$want_code" && "$result" == "$want_result" && "$restarted" == "$want_restart" ]]; then
    echo "PASS $name"
  else
    echo "FAIL $name: codigo=$code result=$result restart=$restarted"
    sed 's/^/  | /' "$work/stdout"
    failures=$(( failures + 1 ))
  fi
}

run "servico vazio e recusado" 2 refused nao SERVICE=
run "nome com comando embutido e recusado" 2 refused nao "SERVICE=flag-service; echo invadido"
run "servico fora da lista e recusado" 2 refused nao SERVICE=postgres-targeting
run "cooldown invalido e recusado" 2 refused nao SERVICE=flag-service COOLDOWN_SECONDS=dez
run "primeiro restart acontece" 0 restarted sim SERVICE=flag-service
run "restart recente respeita o cooldown" 0 cooldown nao SERVICE=flag-service "FAKE_RESTARTED_AT=$(iso_ago 60)" COOLDOWN_SECONDS=600
run "restart antigo libera novo restart" 0 restarted sim SERVICE=flag-service "FAKE_RESTARTED_AT=$(iso_ago 3600)" COOLDOWN_SECONDS=600
run "rollout que nao termina falha" 1 failed sim SERVICE=evaluation-service FAKE_STATUS_EXIT=1

# A allowlist nao pode repetir o valor recusado no log (texto arbitrario).
: > "$work/log"
env FAKE_LOG="$work/log" KUBECTL="$work/kubectl" "SERVICE=<script>x</script>" bash ./restart.sh > "$work/stdout" 2>&1 || true
if grep -q "<script>" "$work/stdout"; then
  echo "FAIL valor recusado aparece no log"
  failures=$(( failures + 1 ))
else
  echo "PASS valor recusado nao aparece no log"
fi

if (( failures > 0 )); then
  echo "$failures teste(s) falharam."
  exit 1
fi
echo "Todos os testes do self-healing passaram."
