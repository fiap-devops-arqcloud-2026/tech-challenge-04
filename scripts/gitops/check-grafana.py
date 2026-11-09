#!/usr/bin/env python3
"""Confere os arquivos do Grafana que o GitOps entrega por ConfigMap.

O Kustomize embute dashboards e alertas como TEXTO: um JSON ou YAML
quebrado renderiza sem erro e so falha dentro do Grafana, no cluster.
Este script le cada arquivo e cruza as referencias entre eles, que sao
os pontos onde uma edicao pequena quebra a cadeia em silencio:

- dashboard: JSON valido, uid unico, ids de painel unicos, painel dentro
  da grade de 24 colunas e sem sobreposicao, datasource conhecida e
  consulta preenchida;
- kustomization: todo dashboard da pasta entra no configMapGenerator;
- alertas: YAML valido, regra apontando para dashboard e painel que
  existem, datasource conhecida, rota da policy apontando para contact
  point que existe e matcher de alertname casando com uma regra real.

As datasources conhecidas vem do values do kube-prometheus-stack, a
mesma fonte que o Grafana usa, e nao de uma lista fixa aqui.

Uso: python3 scripts/gitops/check-grafana.py [pasta gitops/observability]
Sai com 0 se tudo estiver certo e com 1 se houver erro.
"""
import json
import pathlib
import sys

import yaml

GRID_COLUMNS = 24
# Datasource interna do Grafana para expressoes (threshold, math).
EXPRESSION_UID = "__expr__"


def load_yaml(path, errors):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        errors.append(f"{path}: YAML invalido: {exc}")
        return {}


def known_datasources(root, errors):
    values = load_yaml(root / "values" / "kube-prometheus-stack.yaml", errors)
    grafana = values.get("grafana", {})
    uids = set()
    default_uid = grafana.get("sidecar", {}).get("datasources", {}).get("uid")
    if default_uid:
        uids.add(default_uid)
    for source in grafana.get("additionalDataSources", []) or []:
        if source.get("uid"):
            uids.add(source["uid"])
    if not uids:
        errors.append("values/kube-prometheus-stack.yaml: nenhuma datasource com uid encontrada")
    return uids


def check_dashboard(path, datasources, errors):
    """Devolve (uid, ids dos paineis) ou None se o JSON nao abrir."""
    try:
        dashboard = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: JSON invalido: {exc}")
        return None

    uid = dashboard.get("uid")
    if not uid:
        errors.append(f"{path.name}: dashboard sem uid")

    panel_ids = set()
    # Celula da grade -> indice do painel que a ocupa. O indice, e nao o
    # titulo, porque dois paineis podem ter o mesmo titulo.
    occupied = {}
    panels = dashboard.get("panels", [])
    for index, panel in enumerate(panels):
        title = panel.get("title", "?")
        label = f"{path.name}: painel '{title}'"

        panel_id = panel.get("id")
        if panel_id in panel_ids:
            errors.append(f"{label}: id {panel_id} repetido")
        panel_ids.add(panel_id)

        grid = panel.get("gridPos", {})
        x, y = grid.get("x", 0), grid.get("y", 0)
        w, h = grid.get("w", 0), grid.get("h", 0)
        if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > GRID_COLUMNS:
            errors.append(f"{label}: gridPos fora da grade de {GRID_COLUMNS} colunas: {grid}")
        else:
            overlaps = set()
            for cx in range(x, x + w):
                for cy in range(y, y + h):
                    owner = occupied.setdefault((cx, cy), index)
                    if owner != index:
                        overlaps.add(owner)
            for owner in sorted(overlaps):
                errors.append(f"{label}: sobrepoe o painel '{panels[owner].get('title', '?')}'")

        # Paineis de texto e linhas de agrupamento nao consultam dados.
        if panel.get("type") in ("row", "text"):
            continue

        targets = panel.get("targets", [])
        sources = [panel.get("datasource")] + [t.get("datasource") for t in targets]
        for source in filter(None, sources):
            if source.get("uid") not in datasources:
                errors.append(f"{label}: datasource '{source.get('uid')}' nao existe no Grafana")

        if not targets or any(not str(t.get("expr", "")).strip() for t in targets):
            errors.append(f"{label}: consulta (expr) vazia ou ausente")

    return uid, panel_ids


def check_kustomization(root, dashboard_files, errors):
    kustomization = load_yaml(root / "kustomization.yaml", errors)
    listed = set()
    for generator in kustomization.get("configMapGenerator", []) or []:
        for entry in generator.get("files", []) or []:
            # Aceita tambem a forma "chave=caminho".
            listed.add(pathlib.PurePosixPath(entry.split("=", 1)[-1]).as_posix())
    for path in dashboard_files:
        relative = path.relative_to(root).as_posix()
        if relative not in listed:
            errors.append(f"{relative}: dashboard fora do configMapGenerator; nao chegaria ao Grafana")


def walk_routes(policy):
    yield policy
    for route in policy.get("routes", []) or []:
        yield from walk_routes(route)


def check_alerting(root, dashboards, datasources, errors):
    alerting = root / "grafana" / "alerting"
    contact_points = set()
    rule_titles = set()
    policies = []
    for path in sorted(alerting.glob("*.yaml")):
        content = load_yaml(path, errors)
        for point in content.get("contactPoints", []) or []:
            contact_points.add(point.get("name"))
        policies.extend(content.get("policies", []) or [])
        for group in content.get("groups", []) or []:
            for rule in group.get("rules", []) or []:
                title = rule.get("title", "?")
                rule_titles.add(title)
                label = f"{path.name}: regra '{title}'"
                for query in rule.get("data", []) or []:
                    uid = query.get("datasourceUid")
                    if uid != EXPRESSION_UID and uid not in datasources:
                        errors.append(f"{label}: datasource '{uid}' nao existe no Grafana")
                dashboard_uid = rule.get("dashboardUid")
                if dashboard_uid:
                    if dashboard_uid not in dashboards:
                        errors.append(f"{label}: dashboard '{dashboard_uid}' nao existe")
                    elif rule.get("panelId") not in dashboards[dashboard_uid]:
                        errors.append(f"{label}: painel {rule.get('panelId')} nao existe em '{dashboard_uid}'")

    for policy in policies:
        for route in walk_routes(policy):
            receiver = route.get("receiver")
            if receiver and receiver not in contact_points:
                errors.append(f"policies: receiver '{receiver}' nao e um contact point")
            # Matcher no formato [nome, operador, valor]. Uma rota que
            # filtra por alertname deixa de disparar em silencio se a regra
            # for renomeada; e o caso da rota do self-healing.
            for matcher in route.get("object_matchers", []) or []:
                if len(matcher) == 3 and matcher[0] == "alertname" and matcher[1] == "=":
                    if matcher[2] not in rule_titles:
                        errors.append(f"policies: rota para alertname '{matcher[2]}', mas nenhuma regra tem esse titulo")


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "gitops/observability")
    errors = []
    datasources = known_datasources(root, errors)

    dashboard_files = sorted((root / "grafana" / "dashboards").glob("*.json"))
    dashboards = {}
    for path in dashboard_files:
        result = check_dashboard(path, datasources, errors)
        if result and result[0]:
            if result[0] in dashboards:
                errors.append(f"{path.name}: uid '{result[0]}' repetido em outro dashboard")
            dashboards[result[0]] = result[1]

    check_kustomization(root, dashboard_files, errors)
    check_alerting(root, dashboards, datasources, errors)

    for error in errors:
        print(f"[ERRO] {error}")
    if errors:
        print(f"{len(errors)} problema(s) nos arquivos do Grafana.")
        return 1
    print(f"Grafana ok: {len(dashboards)} dashboard(s), alertas e referencias conferidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
