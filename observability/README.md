# Observabilidade — Fase 4

TL;DR: os cinco serviços enviam traces OTLP/HTTP a um OTel Collector. No laboratório local, o Collector remove atributos fora da lista permitida e grava OTLP JSON por linha, com Moto no lugar de SQS/DynamoDB, sem exigir AWS. Logs JSON das aplicações contêm `trace_id`/`span_id` quando existe contexto ativo. No cluster, a mesma instrumentação alimenta Prometheus, Loki, Grafana e New Relic (seção do cluster, abaixo).

Última atualização: 2026-11-09. Este documento descreve a implementação e sua reprodução.

## Entenda o caminho

Uma chamada com cache vazio percorre `evaluation → flag/targeting → auth`. Os bancos e Redis têm spans de dependência. O envio SQS cria um span produtor; seus identificadores seguem nos atributos `traceparent`/`tracestate` da mensagem. O analytics extrai esse contexto e cria o span consumidor e os spans de persistência/ack. A resposta HTTP continua sem esperar pelo processamento analítico.

O corpo JSON de negócio e o item DynamoDB não recebem campos de tracing. Um acerto no cache evita chamadas a flag/targeting/auth; é esperado que esse trace tenha menos serviços.

```text
SDKs Go/Python ── OTLP HTTP :4318/v1/traces ──► Collector
                                                │
                   memory_limiter → health filter → sanitize → batch
                                                │
                              debug básico + arquivo traces.jsonl
```

O arquivo é uma evidência local de diagnóstico, não um backend consultável como o New Relic. Ainda não há envio ao APM, métricas de aplicação/infraestrutura, coleta de logs pelo Collector, Loki, Prometheus ou Grafana nesta composição. Esses componentes continuam nas etapas seguintes do plano.

## Executar o ensaio completo

Pré-requisitos: engine Linux do Docker, Docker Compose, Bash e `python3` no PATH. No Windows, usar Git Bash com Python 3 instalado; o script explicita `COMPOSE_PATH_SEPARATOR` para funcionar com o Docker nativo do Windows. As portas de dados/aplicações definidas no Compose devem estar livres; um nome de projeto diferente não evita conflito de portas.

```bash
bash scripts/test-observability.sh
```

Esse comando valida a configuração do Collector com seu próprio binário, constrói/inicia o laboratório, executa a regressão funcional e depois a prova de traces. Reutiliza o projeto `tc04-integration` do teste da base; não execute os dois testes simultaneamente. A chave fictícia gerada para autenticar os serviços permanece somente na memória dos processos/contêiner e não é impressa.

O ensaio confere:

- saúde, autenticação, persistência, regras e cache dos cinco serviços;
- eventos persistidos pelo consumidor e fila esvaziada;
- um `trace_id` controlado nos cinco serviços, com árvore HTTP e pai produtor SQS → consumidor;
- resposta de negócio preservada e ausência de instrumentação duplicada do endpoint de avaliação;
- logs JSON correlacionados dos cinco serviços;
- remoção de valores sentinela sintéticos em URL/query, headers, SQL/DSN, atributos particulares e mensagens de exceção antes da gravação.

Saída padrão ignorada pelo Git: `00_COLAB_IA/02_TRABALHO/qa-otel/traces.jsonl` e `resultado-traces.json`. Pode escolher outra pasta de QA com `OTEL_TRACE_DIR`, relativa à raiz do repositório ou absoluta. No Linux o script configura UID/GID do operador para permitir escrita no bind mount, sem tornar a pasta gravável por todos. Se executar Compose manualmente, configure `OTEL_UID`/`OTEL_GID` compatíveis com o proprietário da pasta.

```bash
# Opcional: separar as evidências de uma execução.
OTEL_TRACE_DIR=./00_COLAB_IA/02_TRABALHO/qa-otel-minha-execucao bash scripts/test-observability.sh
```

O Collector não tem shell/curl para um healthcheck Docker. A composição aguarda o início do processo; a prova HTTP verifica a extensão real em `127.0.0.1:13133`. SDKs fazem envio em lote, portanto os testes aguardam a exportação em vez de assumir gravação imediata.

## Configuração e privacidade

| Item | Comportamento local |
|---|---|
| Ativação | Endpoint OTLP explícito; `OTEL_SDK_DISABLED=true` desliga o SDK |
| Identidade | `OTEL_SERVICE_NAME` distinto por serviço; ambiente `local` |
| Transporte | OTLP/HTTP protobuf, rede Docker interna; portas de diagnóstico publicadas só em `127.0.0.1` |
| Amostragem do ensaio | `parentbased_always_on`; contexto W3C, sem baggage |
| `/health` | Excluído na instrumentação e filtrado no Collector |
| Saída | Traces em arquivo e contagens no debug; logs JSON da aplicação no stdout |
| Dados | Sem captura intencional de headers/corpos/parâmetros SQL; Collector mantém somente atributos permitidos e limpa mensagens de status/exceção |

A sanitização aplica-se à saída desta configuração do Collector. Não transforma qualquer destino futuro em seguro automaticamente: antes de habilitar exportação externa, reutilizar e verificar o mesmo tratamento. Nomes de spans e campos permitidos também precisam continuar estáticos/controlados. Não configurar headers sensíveis para captura automática. Logs de bibliotecas/servidor podem ter formato diferente dos eventos JSON das aplicações.

Versão do Collector: `0.163.2`, fixada também por digest em `docker-compose.otel.yaml`. Dependências SDK/instrumentadores estão fixadas nos `go.mod`/`requirements.txt` de cada serviço. Go usa instrumentação HTTP e spans manuais de dependências; Python usa Flask/requests/psycopg2 e spans manuais no consumidor, evitando instrumentar a mesma operação duas vezes.

## Encerrar somente o laboratório

Antes, confira a identidade e se são recursos descartáveis desta execução:

```bash
docker ps -a --filter label=com.docker.compose.project=tc04-integration
docker volume ls --filter label=com.docker.compose.project=tc04-integration
docker compose --env-file .env.example -p tc04-integration \
  -f docker-compose.yaml -f docker-compose.integration.yaml -f docker-compose.otel.yaml \
  down -v --remove-orphans
```

O último comando remove os contêineres/rede/volumes descartáveis desse projeto. O arquivo de traces no bind mount permanece na pasta de QA. Não usar `docker system prune` ou comandos globais para limpar este ensaio. A retenção/remoção das evidências locais pode ser decidida separadamente.

## Exportar para o New Relic

O mesmo ensaio pode enviar os traces ao New Relic (conta US). Dois arquivos fazem isso sem mudar a configuração local:

- `observability/otel-collector-newrelic.yaml`: acrescenta o exporter `otlp_http/newrelic` (`https://otlp.nr-data.net`, header `api-key`). Entra como segundo `--config`, então os traces passam pelos mesmos processadores de sanitização antes de sair.
- `docker-compose.newrelic.yaml`: monta esse arquivo no Collector e lê `NEW_RELIC_LICENSE_KEY`. Sem a variável, o Compose para com erro.

A chave é do tipo **Ingest - License** e fica só no `.env` local, que o Git ignora. Nunca no chat, em prints nem em arquivo versionado.

```bash
# No Windows (Git Bash), indicar o Python: PYTHON="py -3"
PYTHON="py -3" bash scripts/test-observability-newrelic.sh
```

O script valida as duas configurações com o binário do Collector, sobe o laboratório, executa as mesmas provas do ensaio local e procura falhas de exportação nos logs do Collector. Depois, no New Relic: **APM & Services > Services - OpenTelemetry** (os cinco serviços), **Service map** e **Distributed tracing**. Para encerrar, usar o comando da seção anterior acrescentando `-f docker-compose.newrelic.yaml`.

Esta prova vale para o ambiente local. O cluster, as métricas, os logs, os alertas e os incidentes continuam nas etapas seguintes.

Fontes primárias consultadas em 2026-10-22: [Collector configuration](https://opentelemetry.io/docs/collector/configuration/), [Transform Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.163.0/processor/transformprocessor), [File Exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.163.0/exporter/fileexporter), [release 0.163.2](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.163.2), [Compose environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/).

## No cluster (EKS)

No cluster, a mesma instrumentação ganha a stack completa: métricas, logs, alertas e incidente. Tudo é implantado pelo ArgoCD a partir de `gitops/observability/`, e os segredos vêm do Terraform (`terraform/k8s/observability.tf`).

A configuração foi validada localmente (ver "Validações locais" abaixo) e entra no ar junto com o cluster.

```text
5 serviços ──OTLP/HTTP──► otel-gateway (Collector central)
                              ├─ traces ──────────► New Relic (Service Map, trace distribuído)
                              ├─ span_metrics ────► Prometheus (requisições, erros, latência)
                              └─ logs ────────────► Loki
otel-agent (DaemonSet) ── logs dos pods ──► otel-gateway
kubelet/cAdvisor ─────────────────────────► Prometheus (CPU e memória dos pods)
Grafana: dashboard + regra de alerta ──► PagerDuty (incidente) + Slack (detalhes)
                                     └─► GitHub (repository_dispatch) ─► self-healing.yml ─► rollout restart
```

| Peça | Chart (versão fixada) | Arquivo de values |
|---|---|---|
| Prometheus + Grafana 13.3.0 | `kube-prometheus-stack` 92.17.1 | `gitops/observability/values/kube-prometheus-stack.yaml` |
| Loki (SingleBinary) | `loki` 7.5.0 | `gitops/observability/values/loki.yaml` |
| Collector gateway | `opentelemetry-collector` 0.178.2 (Collector 0.163.2) | `gitops/observability/values/otel-gateway.yaml` |
| Collector agente | `opentelemetry-collector` 0.178.2 (Collector 0.163.2) | `gitops/observability/values/otel-agent.yaml` |

O dashboard **ToggleMaster - Visao geral** e os alertas ficam versionados em `gitops/observability/grafana/` e chegam ao Grafana como ConfigMaps lidos pelos sidecars do chart.

Acesso durante a gravação, sem Ingress (`localhost:3000`):

```bash
kubectl -n observability port-forward svc/grafana 3000:80
```

Usuário `admin`; a senha é gerada pelo Terraform e fica no Secret `grafana-admin`:

```bash
kubectl -n observability get secret grafana-admin -o jsonpath='{.data.admin-password}' | base64 -d
```

### Alerta, incidente e self-healing

- **Regra `FlagService5xxAlto`:** proporção de respostas 5xx do flag-service acima de 10% por 1 minuto. A conta usa spans SERVER com `STATUS_CODE_ERROR`, que é como uma resposta 5xx aparece nos traces. Sem tráfego, o estado fica OK.
- **Contact points:** `togglemaster-incidente` (PagerDuty e Slack) e `togglemaster-self-healing` (API do GitHub). Os segredos entram como variáveis de ambiente (`$PAGERDUTY_INTEGRATION_KEY`, `$SLACK_WEBHOOK_URL`, `$GITHUB_DISPATCH_TOKEN`). O Git guarda só os nomes.
- **Self-healing:** o workflow `.github/workflows/self-healing.yml` assume uma role AWS por OIDC, cuja única permissão é descrever o cluster, e roda `scripts/self-healing/restart.sh`. O script tem lista de serviços permitidos, intervalo mínimo de 10 minutos entre reinícios e confere o rollout. No cluster, o RBAC só permite reiniciar os 5 Deployments.
- **Fim do incidente:** quando a proporção volta abaixo do limite, o Grafana envia o resolve ao PagerDuty e o incidente fecha sozinho.

### Runbook flag-service 5xx

1. Confirmar no dashboard (painel **Taxa de erro (5xx) por servico**) e nos logs do Loki (`{k8s_namespace_name="togglemaster"}`) quando a falha começou.
2. Acompanhar o self-healing na aba **Actions** do repositório: o job registra o motivo, o resultado (`restarted`, `cooldown`, `refused` ou `ignored`) e os pods depois do reinício.
3. Ver a troca de pods: `kubectl -n togglemaster get pods -l app=flag-service -w`.
4. Se o alerta continuar depois do reinício, a causa não é um estado em memória. Investigar pelo trace no New Relic e pelos logs antes de reiniciar de novo, porque o intervalo mínimo impede reinícios seguidos.

### Validações locais (2026-11-03)

- `helm template` dos 4 charts com o helm do ArgoCD v2.13.2 (imagem oficial do Argo), nas versões e values acima: renderização sem erro. A v2.13.9, instalada desde 2026-11-09, embute o mesmo helm 3.15.4, então o resultado vale para ela.
- `otelcol-contrib validate` (0.163.2) nas configurações finais do gateway e do agente, extraídas do `helm template`.
- Grafana 13.3.0 sem rede, com os arquivos de `gitops/observability/grafana/`. Ele carregou os 2 contact points com as 3 integrações, a política, a regra, os templates, o dashboard e as datasources. Pela API de teste de templates, o corpo enviado ao GitHub sai como `{"event_type":"self-healing","client_payload":{...}}`.
- O mesmo teste mostrou que o Grafana transforma em número um segredo que pareça número, e não sobe. Por isso o Terraform recusa uma Integration Key do PagerDuty nesse formato.

Fontes primárias consultadas em 2026-11-03: values e Chart.yaml de [kube-prometheus-stack 92.17.1](https://github.com/prometheus-community/helm-charts/tree/kube-prometheus-stack-92.17.1/charts/kube-prometheus-stack), [loki 7.5.0](https://github.com/grafana/loki/tree/helm-loki-7.5.0/production/helm/loki) e [opentelemetry-collector 0.178.2](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/opentelemetry-collector-0.178.2/charts/opentelemetry-collector); [provisionamento de alerting do Grafana](https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/); [receptor OTLP do Prometheus](https://prometheus.io/docs/guides/opentelemetry/); [repository_dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event).
