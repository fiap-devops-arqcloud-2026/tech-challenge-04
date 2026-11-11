# 📸 Evidências — Fase 4

TL;DR: são 11 prints do ensaio integrado de 2026-11-09 e os registros da gravação de 2026-11-11. Os quatro prints que o enunciado exige (p. 6) estão marcados com ★, e todos entram no [relatório de entrega](../relatorio/README.md).

Última atualização: 2026-11-11.

## Prints do ensaio de 2026-11-09

O ensaio usou a mesma implantação da gravação. Horários em America/Sao_Paulo (UTC-03), salvo quando indicado UTC.

| Arquivo | O que mostra | No relatório |
|---|---|---|
| ★ [01-grafana-requisicoes.png](2026-11-09/01-grafana-requisicoes.png) | Dashboard ToggleMaster - Visao geral: erros 5xx, requisições por segundo, latência p95 e CPU/memória dos nós | p. 6 |
| ★ [01-grafana-recursos-logs.png](2026-11-09/01-grafana-recursos-logs.png) | O mesmo dashboard: CPU e memória por pod e logs do Loki com `trace_id` | p. 7 |
| ★ [02-trace-spans.png](2026-11-09/02-trace-spans.png) | New Relic: trace de `GET /evaluate` com 19 spans e 56,63 ms, às 18:28 UTC | p. 8 |
| [02-trace-mapa.png](2026-11-09/02-trace-mapa.png) | O mesmo trace no mapa de entidades: 10 entidades, incluindo SQS → analytics → DynamoDB | p. 9 |
| ★ [03-chatops.png](2026-11-09/03-chatops.png) | Slack `#incidentes-tech-challenge`: alerta `FlagService5xxAlto` resolvido às 16:01 | p. 10 |
| ★ [04-self-healing-log.png](2026-11-09/04-self-healing-log.png) | GitHub Actions: passo **Reiniciar com allowlist e cooldown**, com o restart e o rollout | p. 11 |
| [04-self-healing.png](2026-11-09/04-self-healing.png) | Resumo da execução 42679005683: disparada por `repository_dispatch`, sucesso em 43 s | p. 12 |
| [07-grafana-firing.png](2026-11-09/07-grafana-firing.png) | Regra `FlagService5xxAlto` em Firing: a razão de 5xx sobe de 0 para 1 | p. 13 |
| [08-pagerduty.png](2026-11-09/08-pagerduty.png) | Incidente #4 no PagerDuty: aberto às 3:59 PM e resolvido às 4:01 PM | p. 13 |
| [05-argocd.png](2026-11-09/05-argocd.png) | ArgoCD v2.13.9: seis Applications Synced/Healthy | p. 14 |
| [06-lens-nos.png](2026-11-09/06-lens-nos.png) | Lens: os dois nós do EKS com Kubernetes v1.34 | p. 14 |

## Registros da gravação de 2026-11-11

Não são prints. São registros consultados depois da gravação para montar a linha do tempo da p. 5 do relatório:

| Horário | Evento | Fonte |
|---|---|---|
| 00:58:48 | `fault.enabled` no flag-service; primeira resposta 503 | Loki, pods `flag-service` e `trafego` |
| 01:00:50 | Alerta em Firing | Mensagem do Grafana no Slack |
| 01:00:53 | `repository_dispatch` cria a [execução 42956432177](https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04/actions/runs/42956432177) | GitHub Actions |
| 01:01:04 | PagerDuty publica o incidente no Slack | API do Slack |
| 01:01:09 | `deployment.apps/flag-service restarted` | Log da execução |
| 01:01:38 | Primeira resposta HTTP 200 depois da falha | Loki, pod `trafego` |
| 01:03:00 | Alerta Resolved | Mensagem do Grafana no Slack |

No total, o gerador de tráfego registrou 159 respostas 503.

Os mesmos dados podem ser consultados de novo:
- **Log da execução:** `gh run view 42956432177 --log`.
- **Loki:** consulta `{k8s_namespace_name="togglemaster", service_name="trafego"} |= "-> 503"`, enquanto o cluster existir.

## Prints novos

Salve em [entrada-local/](entrada-local/LEIA-ME.md), que é ignorada pelo Git. Antes de mover uma imagem para uma pasta datada, cubra chaves, tokens e e-mails.
