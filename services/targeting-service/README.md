# targeting-service (Python)

> Fase 4 (2026-10-22): este serviço agora possui tracing local e logs JSON. A execução integrada atual usa simuladores locais e credenciais fictícias do laboratório; não exige nova conta AWS. As instruções AWS herdadas abaixo descrevem a integração real e não comprovam implantação. Código e comandos de negócio foram preservados; veja a seção de observabilidade ao final.

Este é o serviço de regras de segmentação (targeting) do projeto ToggleMaster. Ele é responsável por gerenciar regras complexas (ex: "50% dos usuários", "usuários do país X") para uma feature flag específica.

**IMPORTANTE:** Este serviço também é protegido e depende que o `auth-service` esteja rodando (ex: em `http://localhost:8001`).

## 📦 Pré-requisitos (Local)

* [Python](https://www.python.org/) (versão 3.12, a mesma da imagem `python:3.12-slim` e do CI)
* [PostgreSQL](https://www.postgresql.org/download/)
* O `auth-service` deve estar rodando.

## 🚀 Rodando Localmente

1.  **Clone o repositório** e entre na pasta `targeting-service`.

2.  **Prepare o Banco de Dados:**
    * Crie um banco de dados no seu PostgreSQL (ex: `targeting_db`).
    * Execute o script `db/init.sql` para criar a tabela `targeting_rules`:
        ```bash
        psql -U seu_usuario -d targeting_db -f db/init.sql
        ```

3.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz desta pasta (`targeting-service/`) com o seguinte conteúdo:
    ```.env
    # String de conexão do seu banco de dados PostgreSQL
    DATABASE_URL="postgres://SEU_USUARIO:SUA_SENHA@localhost:5432/targeting_db"
    
    # Porta que este serviço (targeting-service) irá rodar
    PORT="8003"
    
    # URL do auth-service (que deve estar rodando na porta 8001)
    AUTH_SERVICE_URL="http://localhost:8001"
    ```

4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Inicie o Serviço:**
    ```bash
    gunicorn --bind 0.0.0.0:8003 app:app
    ```
    O servidor estará rodando em `http://localhost:8003`.

## 🧪 Testando os Endpoints

Lembre-se de obter sua `SUA_CHAVE_API` no `auth-service` (veja o README do `flag-service`).

**1. Verifique a Saúde (Health Check):**
```bash
curl http://localhost:8003/health
```
Saída esperada: `{"status":"ok"}`

**2. Crie uma nova Regra de Segmentação:** Vamos criar uma regra para a flag enable-new-dashboard (que você criou no flag-service). Esta regra fará a flag aparecer para 50% dos usuários.
```bash
curl -X POST http://localhost:8003/rules \
-H "Content-Type: application/json" \
-H "Authorization: Bearer SUA_CHAVE_API" \
-d '{
    "flag_name": "enable-new-dashboard",
    "is_enabled": true,
    "rules": {
        "type": "PERCENTAGE",
        "value": 50
    }
}'
```
Saída esperada: (Um JSON com os dados da regra criada).

**3. Busque a Regra que você criou:**
```bash
curl http://localhost:8003/rules/enable-new-dashboard \
-H "Authorization: Bearer SUA_CHAVE_API"
```
Saída esperada: (O JSON da regra que você acabou de criar).

**4. Atualize a Regra (mude para 75%):**
```bash
curl -X PUT http://localhost:8003/rules/enable-new-dashboard \
-H "Content-Type: application/json" \
-H "Authorization: Bearer SUA_CHAVE_API" \
-d '{
    "rules": {
        "type": "PERCENTAGE",
        "value": 75
    }
}'
```
Saída esperada: (O JSON da regra atualizada, com `"value": 75`).


## Observabilidade local — Fase 4

Última atualização: 2026-10-22. Fonte operacional: `app.py`, `telemetry.py`, `requirements.txt`, `Dockerfile` e `tests/test_telemetry.py` deste serviço; [overlay local](../../docker-compose.otel.yaml).

O serviço cria spans OpenTelemetry somente quando `OTEL_EXPORTER_OTLP_ENDPOINT` ou `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` é informado. `OTEL_SDK_DISABLED=true` tem precedência e desliga a instrumentação/exportação. Sem endpoint, a aplicação continua com seus contratos anteriores e logs JSON, sem tentar contactar um Collector. O código usa o exporter **OTLP HTTP/protobuf**; não foi acrescentado SDK de métricas nem exportação de logs neste passo.

| Variável | Uso |
|---|---|
| `OTEL_SERVICE_NAME` | Nome do recurso; padrão `targeting-service` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Base HTTP do Collector; na rede Compose, `http://otel-collector:4318` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Alternativa com caminho completo `/v1/traces`; precede o endpoint-base |
| `OTEL_RESOURCE_ATTRIBUTES` | Metadados aceitos pelo SDK, por exemplo `deployment.environment.name=local` |
| `OTEL_SDK_DISABLED` | `true` desliga; ausência/`false` exige ainda um endpoint explícito |

Fora dos contêineres, usar o endereço acessível pelo processo; no laboratório com a porta publicada no host, a base é `http://127.0.0.1:4318`. Não há chave ou exporter New Relic nesta etapa. O `service.name` é definido explicitamente e `service.namespace=togglemaster` é adicionado ao recurso.

A inicialização ocorre no import de `app.py`, no worker do Gunicorn atual, **sem `--preload`**. O pool/worker e o SDK não devem nascer no processo mestre antes do fork. O `CMD` usa `exec gunicorn` para entregar sinais ao servidor; o SDK registra seu shutdown no encerramento normal do processo. Não combinar esta instrumentação programática com `opentelemetry-instrument`, pois isso poderia duplicar spans.

Os logs do aplicativo saem em **JSON no stdout**, com `time`, `level`, `service.name` e `message`. Dentro de um span válido, incluem `trace_id` e `span_id`; fora dele, esses dois campos são omitidos. Eventos e tipos de erro são estáticos/controlados: não registrar Authorization, chaves, DSN, corpo, parâmetros SQL, nome de usuário ou recibos SQS. Mensagens de exceção e stacktraces brutos foram retirados dos logs do aplicativo. Logs internos do servidor/bibliotecas não são prometidos como JSON por essa configuração.

O endpoint `/health` é excluído de tracing. A propagação usa somente W3C `traceparent`/`tracestate`, sem `baggage`. A instrumentação HTTP/DB pode produzir atributos técnicos sensíveis por padrão, como URL completa e detalhes de exceção: o [Collector local](../../observability/otel-collector-local.yaml) aplica a sanitização **antes de persistir**. Portanto, manter esse pipeline ao analisar traces; não trocar diretamente por um exporter externo sem revisar a política de dados.

Flask recebe/extrai o contexto HTTP; requests cria o span `CLIENT` e injeta o contexto na chamada de validação ao auth-service. Psycopg2 é instrumentado **antes** de `SimpleConnectionPool` criar conexões. `capture_parameters=False` e SQLCommenter desligado evitam capturar parâmetros ou alterar as consultas; as transações, respostas e regras de negócio permanecem as da base importada.

Os novos testes executam em memória, sem conta AWS nem chamadas de rede:

```bash
python -m unittest discover -s tests -v
```

Eles verificam contexto HTTP, exclusão de health, opt-in/desligamento e logs seguros/correlacionados; o worker também verifica persistência antes do ack, falha sem ack e mensagens sem contexto. Os testes unitários não substituem o ensaio integrado do repositório com banco, simuladores e Collector reais.

Referências primárias consultadas em 2026-10-22: [OTel Flask](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/flask/flask.html), [requests](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html), [Psycopg2](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/psycopg2/psycopg2.html), [exporters HTTP](https://opentelemetry.io/docs/languages/python/exporters/), [fork/Gunicorn](https://opentelemetry-python.readthedocs.io/en/stable/examples/fork-process-model/README.html), [convenções de mensageria](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/) e metadados oficiais [SDK 1.45.1](https://pypi.org/project/opentelemetry-sdk/1.45.1/) / [instrumentação 0.66b1](https://pypi.org/project/opentelemetry-instrumentation-flask/0.66b1/). As dependências OpenTelemetry foram fixadas nessa família compatível; dependências de negócio herdadas foram mantidas.

### Cursor PostgreSQL — correção verificada em 2026-10-27

A factory `RealDictCursor` é definida na criação do `SimpleConnectionPool`/conexão; os endpoints usam `conn.cursor()` para preservar a factory envolvida pelo OpenTelemetry. Informar `cursor_factory=RealDictCursor` novamente em cada cursor substituía a factory instrumentada e suprimia os spans SQL. As linhas continuam como dicionários e consultas/parâmetros continuam os mesmos. Fonte: `app.py`, instrumentador Psycopg2 0.66b1 e teste de regressão `PostgresTracingTests` deste serviço, conferidos em 2026-10-27.

São seis testes locais neste serviço: o novo teste usa Flask, pool, `RealDictCursor` e instrumentador reais, com conexão/execução SQL simuladas, e exige um span `CLIENT` de `SELECT` filho do span HTTP, resposta em dicionário e ausência dos valores dos parâmetros nos atributos SQL. A prova PostgreSQL real faz parte do ensaio integrado do repositório; o teste em memória não a substitui.
