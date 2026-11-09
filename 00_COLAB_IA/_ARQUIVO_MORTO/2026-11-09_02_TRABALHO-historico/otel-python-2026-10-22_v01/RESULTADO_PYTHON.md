# Resultado da instrumentação Python local — E1

TL;DR: flag, targeting e analytics instrumentados sem modificar o contrato de negócio. Tracing opt-in por endpoint, logs JSON no stdout, propagação W3C sem baggage e continuidade SQS → DynamoDB. Dezoito testes unitários passaram; o ensaio integrado Docker/Collector é responsabilidade do agente principal.

Última atualização: 2026-10-22 12:17 (America/Sao_Paulo, UTC-03:00), Codex, subagente ajustar_gitops04.

## Escopo e preservação

Editados somente `services/{flag-service,targeting-service,analytics-service}/`: `app.py`, `requirements.txt`, `Dockerfile`, `README.md`; criados `telemetry.py` e `tests/test_telemetry.py` em cada serviço. Auxiliares/evidências nesta pasta autorizada. Sem alterações em Compose, scripts comuns, contexto, Terraform, GitOps ou serviços Go; sem Git/índice/commit/push/PR/AWS/deploy/integração externa.

Antes de editar, todos os doze originais foram copiados para `00_COLAB_IA/_ARQUIVO_MORTO/2026-10-22_instrumentacao-python/services/<serviço>/`. O manifesto `preservacao-python.json` contém de-para e SHA-256 original/atual. Os três módulos `telemetry.py` são idênticos: a duplicação é intencional porque cada imagem tem contexto de build independente.

## Comportamento implementado

- Família OTel fixada e confirmada no PyPI em 2026-10-22: API/SDK/exporter OTLP HTTP 1.45.1; Flask/requests/psycopg2 instrumentors 0.66b1. Dependências de negócio herdadas mantidas.
- Endpoint explícito (`OTEL_EXPORTER_OTLP_ENDPOINT` ou sinal específico de traces) habilita tracing; `OTEL_SDK_DISABLED=true` desliga. Sem endpoint, não criar provider/exporter/threads OTel.
- `service.name` por nome real/`OTEL_SERVICE_NAME` e `service.namespace=togglemaster`; demais atributos do recurso aceitam configuração padrão do SDK.
- Inicialização após o fork do Gunicorn atual, pois não existe `--preload`. Dockerfiles usam `exec gunicorn`, preservando o comando de negócio e entregando SIGTERM ao servidor. O SDK encerra via callback normal de shutdown no processo; não há flush síncrono por request.
- Flask SERVER extrai o contexto W3C; requests CLIENT propaga-o até auth. Psycopg2 é instrumentado antes da criação do `SimpleConnectionPool`; `capture_parameters=False` e SQLCommenter desligado.
- Analytics recebe `MessageAttributeNames=[traceparent,tracestate]`, extrai somente strings dos atributos e usa o produtor como pai do span CONSUMER por mensagem. Spans `dynamodb.PutItem` e `sqs.DeleteMessage` são filhos. Sem instrumentação botocore paralela.
- DynamoDB mantém os cinco campos de negócio; ack permanece depois de persistir. Sem contexto na mensagem, processar normalmente com trace novo. Em falha, manter mensagem sem ack, registrar somente classe segura do erro.
- Logs do aplicativo: JSON stdout com time/level/service.name/message, IDs de trace/span apenas em contexto válido e extras controlados route/method/status/error.type. Mensagens de sucesso/erro não contêm nomes de flags, user IDs, recibos, payloads ou mensagens brutas de exceção.
- `/health` excluído dos spans; sem baggage. Só traces neste passo: sem SDK/exporter de métricas ou logs, sem New Relic. Collector aplica allowlist/sanitização antes do arquivo local; auto-instrumentação pode gerar URLs/erros sensíveis antes desse limite, conforme acordo com o agente principal.

## Verificações e limites

| Verificação | Resultado em 2026-10-22 |
|---|---|
| Testes flag | 5/5, `tests-flag-service.log` |
| Testes targeting | 5/5, `tests-targeting-service.log` |
| Testes analytics | 8/8, `tests-analytics-service.log` |
| `compileall -q` nos três diretórios | passou |
| Flake8 fatal (mesmas seleções do CI: E9,F63,F7,F82) | passou, `flake8.log` |
| Bandit `-ll` | passou, 0 achados médios/altos; `bandit.json` |
| `git diff --check` no escopo | passou |
| `pip check` da venv de validação | sem dependências quebradas |
| Igualdade SHA-256 de telemetry.py nos três serviços | confirmada |

Os testes provam um único SERVER Flask com pai W3C, propagação requests em transporte mockado, health sem spans, JSON correlacionado sem sentinelas privadas, desligamento sem exporter, consumer como filho do produtor, Dynamo/ack como filhos do consumer, ordem persistir→ack, falhas sem ack e compatibilidade com mensagens antigas. Clientes AWS são mocks; nenhum teste acessou AWS. SQL/HTTP/brokers reais e exportação efetiva OTLP/Collector dependem do ensaio integrado do agente principal.

A venv é auxiliar local com Python 3.12.14, Flask 2.2.2, Werkzeug 2.3.8, requests 2.28.1, boto3 1.26.50 e OTel fixado. Não substitui os builds Linux dos Dockerfiles. Houve um timeout inicial ao baixar dependências, resolvido na segunda tentativa; `pip-install.log` registra a instalação concluída. Warnings de depreciação Flask/Werkzeug herdados não causaram falhas; não se atualizou o framework de negócio nesta tarefa. Bandit também emite avisos de comentários `nosec` herdados, sem achado médio/alto.

## Fontes primárias consultadas

- Metadados oficiais PyPI: https://pypi.org/pypi/opentelemetry-sdk/json e equivalentes da família (`1.45.1`/`0.66b1`), consultados em 2026-10-22.
- https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/flask/flask.html
- https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html
- https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/psycopg2/psycopg2.html
- https://opentelemetry.io/docs/languages/python/exporters/
- https://opentelemetry-python.readthedocs.io/en/stable/examples/fork-process-model/README.html
- https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/
- https://opentelemetry.io/docs/specs/semconv/db/dynamodb/
- https://docs.aws.amazon.com/boto3/latest/reference/services/sqs/client/receive_message.html

Não confundir testes unitários com demonstração de infraestrutura ou fechamento da Fase 4. O próximo passo é o ensaio integrado do principal, com revisão independente e atualização do handoff.


## Revisão no ambiente Docker e correção dos testes — 2026-10-22 12:20 UTC-03

O agente principal confirmou builds das três imagens Python e executou os testes dentro das imagens. Flag/targeting passaram inicialmente; analytics revelou duas asserções frágeis: o teste inferia `SERVICE` pelo nome do diretório pai, que é `/app` dentro da imagem. Isso fazia o logger de teste e o logger real usarem nomes distintos. O código do aplicativo não foi alterado para acomodar os testes.

Correção: `SERVICE` é agora a constante explícita correspondente a cada serviço em cada arquivo de teste. Isso também melhora a verificação de identidade flag/targeting dentro de Docker. Os três testes foram repetidos na venv local com 5/5, 5/5 e 8/8; logs atualizados em `tests-<serviço>_v02.log`, mantendo os logs iniciais. O principal foi avisado para rebuild/rerun Docker, pois os testes fazem parte do contexto copiado para as imagens. Resultado Docker final e ensaio cross-service devem ser registrados pelo principal, sem presumir aprovação a partir destes testes de host.
