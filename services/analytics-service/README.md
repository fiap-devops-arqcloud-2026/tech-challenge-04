# analytics-service (Python)

> Fase 4 — atualização em 2026-10-22, Codex: este serviço agora possui tracing local e logs JSON. A execução integrada atual usa simuladores locais e credenciais fictícias do laboratório; não exige nova conta AWS. As instruções AWS herdadas abaixo descrevem a integração real e não comprovam implantação. Código e comandos de negócio foram preservados; veja a seção de observabilidade ao final.

Este é o serviço de análise (analytics) do projeto ToggleMaster. Ele é um *worker* de backend e não possui uma API pública (exceto `/health`).

Sua única função é:
1.  Ouvir constantemente a fila do **AWS SQS** (que o `evaluation-service` preenche).
2.  Consumir as mensagens de evento da fila.
3.  Gravar os dados de análise em uma tabela do **AWS DynamoDB**.

## 📦 Pré-requisitos (Local)

* [Python](https://www.python.org/) (versão 3.9 ou superior)
* **Credenciais da AWS:** Este serviço **DEVE** ter credenciais da AWS para acessar SQS e DynamoDB. Configure-as em seu terminal (via `aws configure`) ou defina as variáveis de ambiente:
    * `AWS_ACCESS_KEY_ID`
    * `AWS_SECRET_ACCESS_KEY`
    * `AWS_SESSION_TOKEN` (se estiver usando o AWS Academy)
* **Recursos da AWS:** Você precisa ter criado a Fila SQS e a Tabela DynamoDB no console.

## 🚀 Preparando o DynamoDB

Este serviço espera que uma tabela específica exista no DynamoDB.

**Nome da Tabela:** `ToggleMasterAnalytics`
**Chave Primária (Partition Key):** `event_id` (do tipo String)

Você pode criar esta tabela usando o console da AWS ou com o seguinte comando da AWS CLI:

```bash
aws dynamodb create-table \
    --table-name ToggleMasterAnalytics \
    --attribute-definitions \
        AttributeName=event_id,AttributeType=S \
    --key-schema \
        AttributeName=event_id,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=1,WriteCapacityUnits=1
```
(Nota: O throughput provisionado acima é o mínimo possível, ideal para o free tier/testes).

## 🚀 Rodando Localmente
**1. Clone o repositório** e entre na pasta `analytics-service`.

**2. Configure as Variáveis de Ambiente:** Crie um arquivo chamado `.env` na raiz desta pasta (`analytics-service/`) com o seguinte conteúdo. **Garanta que suas credenciais da AWS também estejam configuradas no seu ambiente.**
```.env
# Porta que este serviço (health check) irá rodar
PORT="8005"

# --- Configuração da AWS ---
# Cole a URL da fila SQS que você criou
AWS_SQS_URL="httpsiso://[sqs.us-east-1.amazonaws.com/123456789012/sua-fila](https://sqs.us-east-1.amazonaws.com/123456789012/sua-fila)"

# Nome da tabela DynamoDB que você criou
AWS_DYNAMODB_TABLE="ToggleMasterAnalytics"

# Região dos seus serviços SQS e DynamoDB
AWS_REGION="us-east-1"
```

**3. Instale as Dependências:**
```bash
pip install -r requirements.txt
```

**4. Inicie o Serviço:**
```bash
gunicorn --bind 0.0.0.0:8005 app:app
```
O servidor estará rodando em `http://localhost:8005`. Você verá logs no terminal assim que o worker SQS iniciar e (eventualmente) processar mensagens.

## 🧪 Testando o Serviço

Testar este serviço é diferente. Você não vai chamar uma API dele.

**1. Verifique a Saúde:**
```bash
curl http://localhost:8005/health
```
Saída esperada: `{"status":"ok"}``

**2. Gere Eventos:**

- Vá para o `evaluation-service` (que deve estar rodando) e faça algumas requisições de avaliação:
```bash
curl "http://localhost:8004/evaluate?user_id=test-user-1&flag_name=enable-new-dashboard"
curl "http://localhost:8004/evaluate?user_id=test-user-2&flag_name=enable-new-dashboard"
```
- **Alternativa:** Envie uma mensagem manualmente pelo Console da AWS SQS.

**3. Observe os Logs:**

No terminal do `analytics-service`, você deverá ver os logs aparecendo, indicando que as mensagens foram recebidas e salvas no DynamoDB:
```bash
INFO:Iniciando o worker SQS...
INFO:Recebidas 2 mensagens.
INFO:Processando mensagem ID: ...
INFO:Evento ... (Flag: enable-new-dashboard) salvo no DynamoDB.
INFO:Processando mensagem ID: ...
INFO:Evento ... (Flag: enable-new-dashboard) salvo no DynamoDB.
```

**4. Verifique o DynamoDB:**

Vá até o console da AWS, abra o **DynamoDB**, selecione a tabela `ToggleMasterAnalytics` e clique em "Explore table items".

Você verá os itens que o worker acabou de inserir.

## Observabilidade local — Fase 4

Última atualização: 2026-10-22, Codex. Fonte operacional: `app.py`, `telemetry.py`, `requirements.txt`, `Dockerfile` e `tests/test_telemetry.py` deste serviço; [overlay local](../../docker-compose.otel.yaml).

O serviço cria spans OpenTelemetry somente quando `OTEL_EXPORTER_OTLP_ENDPOINT` ou `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` é informado. `OTEL_SDK_DISABLED=true` tem precedência e desliga a instrumentação/exportação. Sem endpoint, a aplicação continua com seus contratos anteriores e logs JSON, sem tentar contactar um Collector. O código usa o exporter **OTLP HTTP/protobuf**; não foi acrescentado SDK de métricas nem exportação de logs neste passo.

| Variável | Uso |
|---|---|
| `OTEL_SERVICE_NAME` | Nome do recurso; padrão `analytics-service` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Base HTTP do Collector; na rede Compose, `http://otel-collector:4318` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Alternativa com caminho completo `/v1/traces`; precede o endpoint-base |
| `OTEL_RESOURCE_ATTRIBUTES` | Metadados aceitos pelo SDK, por exemplo `deployment.environment.name=local` |
| `OTEL_SDK_DISABLED` | `true` desliga; ausência/`false` exige ainda um endpoint explícito |

Fora dos contêineres, usar o endereço acessível pelo processo; no laboratório com a porta publicada no host, a base é `http://127.0.0.1:4318`. Não há chave ou exporter New Relic nesta etapa. O `service.name` é definido explicitamente e `service.namespace=togglemaster` é adicionado ao recurso.

A inicialização ocorre no import de `app.py`, no worker do Gunicorn atual, **sem `--preload`**. O pool/worker e o SDK não devem nascer no processo mestre antes do fork. O `CMD` usa `exec gunicorn` para entregar sinais ao servidor; o SDK registra seu shutdown no encerramento normal do processo. Não combinar esta instrumentação programática com `opentelemetry-instrument`, pois isso poderia duplicar spans.

Os logs do aplicativo saem em **JSON no stdout**, com `time`, `level`, `service.name` e `message`. Dentro de um span válido, incluem `trace_id` e `span_id`; fora dele, esses dois campos são omitidos. Eventos e tipos de erro são estáticos/controlados: não registrar Authorization, chaves, DSN, corpo, parâmetros SQL, nome de usuário ou recibos SQS. Mensagens de exceção e stacktraces brutos foram retirados dos logs do aplicativo. Logs internos do servidor/bibliotecas não são prometidos como JSON por essa configuração.

O endpoint `/health` é excluído de tracing. A propagação usa somente W3C `traceparent`/`tracestate`, sem `baggage`. A instrumentação HTTP/DB pode produzir atributos técnicos sensíveis por padrão, como URL completa e detalhes de exceção: o [Collector local](../../observability/otel-collector-local.yaml) aplica a sanitização **antes de persistir**. Portanto, manter esse pipeline ao analisar traces; não trocar diretamente por um exporter externo sem revisar a política de dados.

Cada mensagem extrai contexto dos `MessageAttributes` SQS (strings `traceparent` e `tracestate`) e gera um span `CONSUMER` chamado `sqs.process`, usando o produtor como pai. Como cada mensagem é processada individualmente, não há span de lote servindo de pai artificial. Mensagens antigas sem contexto continuam funcionando e iniciam um trace novo.

`dynamodb.PutItem` e `sqs.DeleteMessage` são spans `CLIENT` filhos do consumidor. O item DynamoDB mantém exatamente `event_id`, `user_id`, `flag_name`, `result` e `timestamp`; nenhum dado de telemetria entra no corpo/item. O ack continua ocorrendo somente após persistência bem-sucedida. Não foi instalada auto-instrumentação botocore, para evitar spans duplicados e captura do payload.

Os novos testes executam em memória, sem conta AWS nem chamadas de rede:

```bash
python -m unittest discover -s tests -v
```

Eles verificam contexto HTTP, exclusão de health, opt-in/desligamento e logs seguros/correlacionados; o worker também verifica persistência antes do ack, falha sem ack e mensagens sem contexto. Os testes unitários não substituem o ensaio integrado do repositório com banco, simuladores e Collector reais.

Referências primárias consultadas em 2026-10-22: [OTel Flask](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/flask/flask.html), [requests](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html), [Psycopg2](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/psycopg2/psycopg2.html), [exporters HTTP](https://opentelemetry.io/docs/languages/python/exporters/), [fork/Gunicorn](https://opentelemetry-python.readthedocs.io/en/stable/examples/fork-process-model/README.html), [convenções de mensageria](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/) e metadados oficiais [SDK 1.45.1](https://pypi.org/project/opentelemetry-sdk/1.45.1/) / [instrumentação 0.66b1](https://pypi.org/project/opentelemetry-instrumentation-flask/0.66b1/). As dependências OpenTelemetry foram fixadas nessa família compatível; dependências de negócio herdadas foram mantidas.
