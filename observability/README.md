# Observabilidade local — Fase 4

TL;DR: os cinco serviços enviam traces OTLP/HTTP a um Collector local. O Collector remove atributos fora da lista permitida e grava OTLP JSON por linha. Logs JSON das aplicações contêm `trace_id`/`span_id` quando existe contexto ativo. O laboratório usa Moto para SQS/DynamoDB e não exige AWS ou New Relic.

Última atualização: 2026-10-22, Codex. Este documento descreve a implementação e sua reprodução; os resultados executados ficam nos relatórios ligados no README principal.

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
