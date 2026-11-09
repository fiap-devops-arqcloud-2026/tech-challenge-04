# auth-service (Go)

Este é o serviço de autenticação do projeto ToggleMaster. Ele é responsável por criar e validar chaves de API.

## 📦 Pré-requisitos (Local)

* [Go](https://go.dev/doc/install) (versão 1.25.0 ou superior)
* [PostgreSQL](https://www.postgresql.org/download/) (rodando localmente ou em um contêiner Docker)

## 🚀 Rodando Localmente

1.  **Clone o repositório** e entre na pasta `auth-service`.

2.  **Prepare o Banco de Dados:**
    * Crie um banco de dados no seu PostgreSQL (ex: `auth_db`).
    * Execute o script `db/init.sql` para criar a tabela `api_keys`:
        ```bash
        psql -U seu_usuario -d auth_db -f db/init.sql
        ```

3.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz desta pasta (`auth-service/`) com o seguinte conteúdo:
    ```.env
    # String de conexão do seu banco de dados PostgreSQL
    DATABASE_URL="postgres://SEU_USUARIO:SUA_SENHA@localhost:5432/auth_db"
    
    # Porta que o serviço irá rodar
    PORT="8001"
    
    # Chave mestra para criar novas chaves de API
    MASTER_KEY="local-master-key-change-me"
    ```

4.  **Instale as Dependências:**
    ```bash
    go mod tidy
    ```

5.  **Inicie o Serviço:**
    ```bash
    go run .
    ```
    O servidor estará rodando em `http://localhost:8001`.

## 🧪 Testando os Endpoints

Você pode usar `curl` ou Postman.

**1. Verifique a Saúde (Health Check):**
```bash
curl http://localhost:8001/health
```

Saída esperada: `{"status":"ok"}`

**2. Crie uma nova Chave de API (requer a MASTER_KEY):**

```bash
curl -X POST http://localhost:8001/admin/keys \
-H "Content-Type: application/json" \
-H "Authorization: Bearer local-master-key-change-me" \
-d '{"name": "meu-primeiro-servico"}'
``` 

Saída esperada (A SUA CHAVE SERÁ DIFERENTE):

```json
{
  "name": "meu-primeiro-servico",
  "key": "tm_key_a1b2c3d4...",
  "message": "Guarde esta chave com segurança! Você não poderá vê-la novamente."
}
```

**3. Valide a Chave que você acabou de criar: (Substitua tm_key_... pela chave exata que você recebeu no passo anterior)**

```bash
curl http://localhost:8001/validate \
-H "Authorization: Bearer tm_key_a1b2c3d4..."
```

Saída esperada: `{"message":"Chave válida"}`

**4. Teste uma Chave Inválida:**

```bash
curl http://localhost:8001/validate \
-H "Authorization: Bearer chave-errada-123"
```

Saída esperada: `Chave de API inválida ou inativa`

## Observabilidade local — 2026-10-27

A instrumentação é opcional. Para exportar traces ao Collector local, configure:

```dotenv
OTEL_SERVICE_NAME=auth-service
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

O endpoint base recebe `/v1/traces`. Como alternativa, `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` define a URL completa e tem precedência. Sem endpoint, ou com `OTEL_SDK_DISABLED=true`, o SDK não exporta traces. O bootstrap Go usa explicitamente OTLP/HTTP; não configura exporters de métricas ou logs.

O middleware cria um span por requisição, recebe `traceparent`/`tracestate` W3C e exclui `/health`. Consultas PostgreSQL usam o contexto da requisição e spans de operação, sem SQL ou parâmetros nos atributos. Os logs JSON no stdout contêm `event` estático, `service.name` e, havendo contexto válido, `trace_id`/`span_id`; não registram nomes, chaves, hashes ou detalhes de erros de banco.

No encerramento por SIGTERM/interrupt, o servidor termina as requisições antes do flush do SDK. Os testes locais usam SQL simulado e receptor OTLP HTTP em memória:

```bash
go test ./...
go vet ./...
```

Fontes em 2026-10-27: [bootstrap e middleware](telemetry.go), [SQL e logs](handlers.go), [testes](telemetry_test.go), [OTLP HTTP 1.46.0](https://pkg.go.dev/go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.46.0). A validação do trace dos cinco serviços é feita pelo ensaio integrado na raiz do projeto.
