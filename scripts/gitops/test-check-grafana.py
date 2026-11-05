#!/usr/bin/env python3
"""Testes do check-grafana.py.

Cada caso copia gitops/observability para uma pasta temporaria, estraga
UMA coisa e confere que o verificador reprova com a mensagem esperada.
O primeiro caso prova o contrario: a pasta real passa. Um verificador
que nunca foi visto reprovando nao prova nada.

Uso: python3 scripts/gitops/test-check-grafana.py
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / "gitops" / "observability"
CHECKER = HERE / "check-grafana.py"
DASHBOARD = "grafana/dashboards/togglemaster-overview.json"
RULES = "grafana/alerting/rules.yaml"
POLICIES = "grafana/alerting/policies.yaml"


def edit_dashboard(change):
    def apply(root):
        path = root / DASHBOARD
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data["panels"])
        path.write_text(json.dumps(data), encoding="utf-8")
    return apply


def replace(relative, pattern, new):
    def apply(root):
        path = root / relative
        text = path.read_text(encoding="utf-8")
        changed, count = re.subn(pattern, new, text, count=1)
        # Se o arquivo real mudar e o trecho sumir, o caso tem de falhar
        # aqui, e nao passar sem ter estragado nada.
        if count != 1:
            raise AssertionError(f"trecho '{pattern}' nao encontrado em {relative}")
        path.write_text(changed, encoding="utf-8")
    return apply


def duplicate_id(panels):
    panels[1]["id"] = panels[0]["id"]


def overlap(panels):
    panels[1]["gridPos"] = dict(panels[0]["gridPos"])


def unknown_datasource(panels):
    panels[0]["datasource"]["uid"] = "inexistente"


def empty_query(panels):
    panels[0]["targets"][0]["expr"] = " "


def truncate_json(root):
    path = root / DASHBOARD
    path.write_text(path.read_text(encoding="utf-8")[:-20], encoding="utf-8")


def extra_dashboard(root):
    data = json.loads((root / DASHBOARD).read_text(encoding="utf-8"))
    data["uid"] = "extra"
    (root / "grafana/dashboards/extra.json").write_text(json.dumps(data), encoding="utf-8")


CASES = [
    ("a pasta real passa", None, 0, "Grafana ok"),
    ("JSON quebrado reprova", truncate_json, 1, "JSON invalido"),
    ("id de painel repetido reprova", edit_dashboard(duplicate_id), 1, "repetido"),
    ("paineis sobrepostos reprovam", edit_dashboard(overlap), 1, "sobrepoe"),
    ("datasource desconhecida reprova", edit_dashboard(unknown_datasource), 1, "'inexistente' nao existe"),
    ("consulta vazia reprova", edit_dashboard(empty_query), 1, "consulta (expr) vazia"),
    ("dashboard fora do kustomization reprova", extra_dashboard, 1, "fora do configMapGenerator"),
    ("regra apontando para painel inexistente reprova", replace(RULES, r"panelId: \d+", "panelId: 999"), 1, "painel 999 nao existe"),
    ("receiver inexistente reprova", replace(POLICIES, r"receiver: togglemaster-self-healing", "receiver: inexistente"), 1, "'inexistente' nao e um contact point"),
    ("regra renomeada sem ajustar a rota reprova", replace(RULES, r"title: FlagService5xxAlto", "title: FlagService5xxRenomeado"), 1, "nenhuma regra tem esse titulo"),
    ("YAML quebrado reprova", replace(RULES, r"(?m)^groups:", "groups: [\n  - :"), 1, "YAML invalido"),
]


def run_case(name, mutate, want_code, want_text):
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp) / "observability"
        shutil.copytree(SOURCE, root)
        if mutate:
            mutate(root)
        result = subprocess.run([sys.executable, str(CHECKER), str(root)],
                                capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    if result.returncode == want_code and want_text in output:
        print(f"PASS {name}")
        return True
    print(f"FAIL {name}: codigo={result.returncode}, esperado={want_code} com '{want_text}'")
    for line in output.splitlines():
        print(f"  | {line}")
    return False


def main():
    failures = sum(not run_case(*case) for case in CASES)
    if failures:
        print(f"{failures} teste(s) falharam.")
        return 1
    print(f"Todos os {len(CASES)} testes do verificador do Grafana passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
