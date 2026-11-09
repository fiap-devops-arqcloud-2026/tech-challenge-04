#!/usr/bin/env bash
# ============================================================
# VALIDACAO DA PASTA gitops/ - local e no workflow GitOps Check
# ============================================================
# O ArgoCD aplica no cluster o que estiver em gitops/. Um erro aqui so
# apareceria na sincronizacao, com o EKS ligado. Este script pega antes:
#
#   1. renderiza cada pasta que tem kustomization.yaml (base, overlay e
#      observabilidade), como o ArgoCD fara;
#   2. confere os arquivos do Grafana, que o Kustomize so embute como
#      texto (scripts/gitops/check-grafana.py);
#   3. roda os testes do proprio verificador do Grafana.
#
# No CI (variavel CI=true, definida pelo GitHub Actions) a falta de uma
# ferramenta e erro. Na maquina local vira aviso, como no validate-all.
# ============================================================
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# Ausencia de ferramenta: erro no CI, aviso local.
missing() {
  if [[ "${CI:-}" == "true" ]]; then
    echo "::error::$1"
    exit 1
  fi
  echo "[AVISO] $1"
}

# ------------------------------------------------------------
# 1. Kustomize
# ------------------------------------------------------------
# kustomize autonomo primeiro (e o que o CI instala, versao fixa); o
# kubectl kustomize embutido serve na maquina local.
render=()
if command -v kustomize >/dev/null 2>&1; then
  render=(kustomize build)
elif command -v kubectl >/dev/null 2>&1; then
  render=(kubectl kustomize)
else
  missing "kustomize e kubectl ausentes; render do GitOps nao verificado."
fi

if (( ${#render[@]} > 0 )); then
  # Toda pasta com kustomization.yaml: uma pasta nova entra sozinha.
  while IFS= read -r dir; do
    echo "[kustomize] ${dir}"
    "${render[@]}" "${dir}" >/dev/null
  done < <(find gitops -name kustomization.yaml -exec dirname {} \; | sort)
fi

# ------------------------------------------------------------
# 2 e 3. Arquivos do Grafana e testes do verificador
# ------------------------------------------------------------
# Mesmo criterio de interpretador do validate-all: python3 no Linux,
# py ou python no Windows.
python_bin=""
for candidato in python3 python py; do
  if command -v "$candidato" >/dev/null 2>&1 && "$candidato" -c "" >/dev/null 2>&1; then
    python_bin="$candidato"
    break
  fi
done

if [[ -z "$python_bin" ]]; then
  missing "Python ausente; arquivos do Grafana nao verificados."
elif ! "$python_bin" -c "import yaml" >/dev/null 2>&1; then
  missing "PyYAML ausente (pip install pyyaml); arquivos do Grafana nao verificados."
else
  echo "[grafana] conferindo dashboards e alertas"
  "$python_bin" scripts/gitops/check-grafana.py gitops/observability
  echo "[grafana] testes do verificador"
  "$python_bin" scripts/gitops/test-check-grafana.py
fi

echo "Validacao do GitOps concluida."
