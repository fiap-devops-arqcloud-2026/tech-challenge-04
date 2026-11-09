# Passo 2 — instrumentação e observabilidade local

TL;DR: os cinco serviços foram instrumentados e aprovados no ensaio real com Collector local. Uma avaliação gerou 19 spans no mesmo trace, incluindo HTTP, PostgreSQL dos três serviços, Redis, produtor/consumidor SQS e DynamoDB. Respostas de negócio, logs correlacionados, tratamento de dados e regressão funcional passaram. Exportação New Relic permanece pendente, conforme a escolha do usuário de validar localmente primeiro.

Última atualização: 2026-10-27, Codex. Execução final aprovada às 11:03 e laboratório encerrado às 11:04, America/Sao_Paulo (UTC-03:00).

## Explicação simples

Acrescentamos identificadores que acompanham uma operação enquanto ela passa pelos serviços. Assim é possível reconstruir seu caminho e localizar quanto tempo cada parte consumiu. O identificador também acompanha a mensagem da fila: a etapa assíncrona continua ligada à avaliação que a originou, mesmo depois da resposta HTTP.

O Collector recebeu esses registros, removeu atributos fora da lista permitida e gravou uma evidência local. O corpo JSON da avaliação e o item de negócio no DynamoDB continuaram iguais. Ainda não há interface APM externa neste ensaio.

## Implementação técnica

| Componente | Aplicação |
|---|---|
| Auth Go | Middleware HTTP, PostgreSQL com QueryRowContext e spans manuais sem SQL/argumentos |
| Evaluation Go | Contexto da requisição em chamadas HTTP/Redis; produtor SQS assíncrono com contexto preservado e timeout de cinco segundos |
| Flag/targeting Python | Flask, requests e psycopg2 instrumentados; cursor em dicionário preservado sem substituir a factory instrumentada |
| Analytics Python | Extração W3C por mensagem, span CONSUMER, spans de PutItem e confirmação SQS; só confirma depois de persistir |
| Contexto | traceparent/tracestate HTTP e MessageAttributes SQS do tipo String; sem baggage e sem campos extras no JSON de negócio |
| Logs da aplicação | JSON no stdout, service.name e trace_id/span_id quando existe contexto; eventos controlados |
| Ciclo de vida | SDK em lote; Go drena handlers/produtores antes do shutdown; Python inicia no worker sem preload e Dockerfile usa exec gunicorn |
| Collector local | OTLP HTTP/gRPC, memory_limiter, filtro health, sanitização, batch e exportação debug básico/arquivo |

SDK/exporter Go `1.46.0`, otelhttp `0.71.0`; SDK/exporter Python `1.45.1`, instrumentadores `0.66b1`. Builds de aplicação aprovados nas imagens Go 1.25 e Python 3.12 dos Dockerfiles. A versão de psycopg2 dos serviços continua `2.9.5`; a QA Windows usou `2.9.11`, e o ensaio Docker conferiu o runtime real. Collector `0.163.2`, fixado pelo digest `sha256:7f22d2a6748110ffb6a59bc0df448bccbf501cdb667d610ede4c61d3863d5849`.

Ativação por endpoint OTLP explícito; `OTEL_SDK_DISABLED=true` permite desligar o SDK. O endpoint base local é `http://otel-collector:4318`, com envio a `/v1/traces`. Portas de diagnóstico OTLP HTTP e health publicadas somente em 127.0.0.1. Não há exporter/chave New Relic nesta configuração.

## Resultados executados

| Verificação | Resultado final |
|---|---|
| Regressão completa da base | Aprovada; sete eventos esperados persistidos e fila esvaziada |
| Avaliação com traceparent controlado e cache vazio | Resposta preservada; mais um evento conferido |
| Distribuição do trace | 19 spans, cinco service.name, IDs únicos e árvore de pais fechada |
| PostgreSQL | CLIENT auth=2, flag=1 e targeting=1, filhos do SERVER do próprio serviço |
| SQS | Um PRODUCER e um CONSUMER; consumidor filho do produtor correto |
| Redis e DynamoDB | Spans das operações presentes no caminho |
| Logs JSON | Cinco serviços correlacionados pelo mesmo trace; chave gerada ausente |
| Sonda de sanitização | Sentinelas removidas de URL/query, headers, SQL/DSN, IDs, atributos particulares e detalhes de exceção/status |
| Sondas /health com contexto explícito | Sem spans persistidos |
| Go | 13 testes principais + oito subtestes; build, vet e gofmt aprovados |
| Python nos contêineres reconstruídos | 20/20: flag 6, targeting 6 e analytics 8 |
| Configuração Collector | Validação do próprio binário aprovada |
| Estabilidade do código durante ensaio final | 28 arquivos de produção com SHA-256 idêntico antes/depois |

## Lacuna encontrada e corrigida na revisão

A primeira prova produziu 17 spans válidos, mas faltavam SELECTs de flag/targeting. `conn.cursor(cursor_factory=RealDictCursor)` substituía a factory envolvida pelo instrumentador. A correção definiu `RealDictCursor` no pool/connect e passou a usar `conn.cursor()` nas rotas, preservando o formato dos dados.

Um teste adicional por serviço exige o span SQL filho do HTTP e a mesma resposta em dicionário. Contra os fontes anteriores, os testes falham pela ausência do SELECT. O ensaio integrado também passou a exigir CLIENT PostgreSQL nos três serviços; o trace antigo de 17 spans não satisfaz esse novo critério. A prova final de 19 spans passou com PostgreSQL real.

Outra correção pequena removeu um falso positivo do verificador de padrões: cópias arquivadas do próprio security-check.sh contêm suas expressões. O script exclui somente esses verificadores no arquivo morto, mantendo os demais arquivos na busca. Saída final 0. Trata-se de verificação limitada de padrões conhecidos, não de auditoria de segurança completa.

## Arquivos, reprodução e evidências

- [Runbook local](../../observability/README.md): requisitos, execução, configuração, limites e limpeza.
- `docker-compose.otel.yaml`, `observability/otel-collector-local.yaml`, `scripts/test-observability.sh`, `scripts/integration/test-traces.py`.
- `services/{auth,evaluation}-service/telemetry.go` e testes Go; `services/{flag,targeting,analytics}-service/telemetry.py` e testes Python; demais fontes e dependências ajustadas nos seus próprios diretórios.
- [Relatório Go](RELATORIO_GO_OTEL_2026-10-27_v01.md), [revisão Python](REVISAO_PYTHON_OTEL_2026-10-27_v01.md) e [revisão independente](REVISAO_TERRAFORM_E_OTEL_2026-10-27_v01.md).
- [Resultado consolidado portátil](RESULTADO_PASSOS_LOCAIS_2026-10-27_v01.json).
- Evidências brutas locais ignoradas: `qa-passos-locais-2026-10-27/passo2-compose-sql-final.log`, `otel/traces.jsonl`, `otel/resultado-traces.json`, testes Docker e `cleanup-result.json`.

```bash
bash scripts/test-observability.sh
```

Requer engine Linux, Compose, Bash e Python 3 funcional no PATH. Nesta máquina foi usado o Python empacotado já instalado, exposto apenas ao processo do teste por um shim na pasta de QA; não houve alteração do PATH global. Git Bash usa separador Compose explícito e preserva o caminho Linux do argumento de validação.

## Relação com os requisitos e limites

Instrumentação dos cinco serviços atende a implementação local de REQ-OBR-13 e usa a preferência OpenTelemetry REQ-BON-02. A prova prepara REQ-OBR-14/15, mas sua aceitação exige exibição no APM. REQ-OBR-11 permanece parcial: esta etapa trata traces e logs correlacionados no stdout; métricas e coleta/exportação de logs aos backends ainda não foram implantadas.

Não houve execução na AWS, Terraform plan/apply, CI remoto, implantação Kubernetes, New Relic, Prometheus/Loki/Grafana, alertas ou self-healing. Logs internos de SDK/Gunicorn podem ter outro formato. O shutdown/flush foi testado em processo e na drenagem Go; não se alega entrega garantida de toda telemetria em encerramento abrupto ou validação SIGTERM ponta a ponta de todos os serviços.

As 39 fontes/entregáveis preexistentes do 04 permanecem intactas por SHA-256; a Fase 3 segue limpa e somente leitura; 33 exclusões anteriores foram mantidas. Branch dev e refs HEAD/main preservadas. Sem commit, push ou PR.

## Encerramento e próximo passo

Foram removidos somente os 12 contêineres e dois volumes descartáveis identificados pelo rótulo do projeto tc04-integration. Nada desse projeto permaneceu ativo; as evidências em bind mount foram preservadas.

P-008 local concluída. E1 externa permanece pendente: disponibilizar conta New Relic, configurar a chave localmente e provar ingestão/trace/mapa no APM. Em paralelo, confirmar conta AWS, backend, orçamento/cotas e identidades para E0/E2. Nenhuma dessas ações foi executada por este ensaio.

Checklist: [x] instrumentação; [x] testes de contrato e contexto; [x] dependências SQL reais; [x] revisão independente; [x] relatório/resumo; [x] preservação e limpeza; [x] contexto/handoff.
