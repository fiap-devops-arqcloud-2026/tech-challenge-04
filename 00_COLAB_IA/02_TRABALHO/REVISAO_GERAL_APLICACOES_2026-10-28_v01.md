# Revisão geral — aplicações, Compose e observabilidade local

TL;DR: os cinco serviços estão conteinerizados e instrumentados, com evidência local válida de integração e tracing. A implementação atual ainda não entrega métricas, coleta central de logs, backends de observabilidade ou APM externo. Uma sonda específica confirmou que falhas do targeting podem liberar uma flag habilitada e responder HTTP 200; esse comportamento precisa ser tratado no desenho dos alertas e do cenário de falha. Esta revisão não modificou o código operacional.

Última atualização: 2026-10-28 09:10 (America/Sao_Paulo, UTC-03:00), Codex / revisao_aplicacoes.

## 1. Escopo, datas e limites

Revisão iniciada em 2026-10-27 e concluída documentalmente em 2026-10-28. Escopo deste parecer: fontes dos cinco serviços, Dockerfiles/dependências, testes, três composições Docker, Collector local e scripts de integração. A matriz integral dos 42 requisitos e a auditoria de Terraform/CI/GitOps são consolidadas pelo agente coordenador.

Fonte normativa de referência: [README de requisitos](../../docs/requisitos/README.md), que aponta página/trecho do enunciado. As referências às páginas abaixo seguem esse mapa; a leitura integral do PDF é responsabilidade do coordenador desta revisão. Não foi consultada nenhuma conta AWS, New Relic, PagerDuty ou Slack.

Os testes integrados e suites de produção citados foram executados em **2026-10-27**, na sessão anterior. Nesta revisão, em 2026-10-27, foram relidos seus resultados, recalculada a árvore do trace bruto e executada uma sonda nova e isolada de cinco cenários do evaluation. Em **2026-10-28**, os hashes de produção foram reconferidos: **28/28 correspondem ao manifesto do ensaio final**, sem divergências. Não foi reexecutado o laboratório integrado.

- [x] Ler contexto e requisitos pertinentes.
- [x] Inspecionar fontes, configurações e testes do escopo.
- [x] Conferir evidências e correspondência com fontes atuais.
- [x] Reproduzir pontualmente o achado de fallback em cópia isolada.
- [x] Separar exigências FIAP, lacunas de implantação e recomendações técnicas.
- [x] VERIFICAÇÃO: referências, números, datas e limites revisados; relatório entregue ao coordenador.

## 2. O que existe e foi comprovado

| Componente | Implementação encontrada | Evidência disponível / limite |
|---|---|---|
| auth-service | API de chaves, PostgreSQL, autenticação, spans SQL com contexto HTTP, JSON correlacionado | Integração real com PostgreSQL local e testes SQL simulados; não comprova RDS atual |
| flag-service | CRUD de flags, validação no auth, PostgreSQL, Flask/requests/psycopg2 instrumentados | SQL real exportado no ensaio; `RealDictCursor` no pool preserva instrumentação |
| targeting-service | CRUD de regras, validação no auth, PostgreSQL, mesmas integrações OTel | SQL real exportado; regras 0%/100% exercitadas na integração |
| evaluation-service | Cache Redis de 30 segundos, consultas paralelas HTTP, cálculo da regra, envio SQS assíncrono | Cache, expiração, propagação HTTP e SQS comprovados localmente; comportamento degradado tem achado A-01 |
| analytics-service | Consumo SQS, persistência DynamoDB antes do ack, contexto por mensagem e spans de dependência | Sete eventos de regressão + um evento controlado via Moto; não comprova serviços AWS reais |
| Collector | Receptor OTLP, memória limitada, exclusão de health, sanitização, batch e gravação de traces | Arquivo JSONL e debug locais; sem exporter New Relic, pipeline de métricas ou pipeline de logs |
| Contêineres | Cinco Dockerfiles, Go 1.25 / Python 3.12, execução não root, Gunicorn via `exec` | Imagens reconstruídas e ensaio aprovado em 2026-10-27; imagens publicadas no destino Fase 4 ainda não evidenciadas aqui |

O padrão atual exporta traces somente quando existe endpoint OTLP explícito e respeita `OTEL_SDK_DISABLED=true`. A propagação é W3C TraceContext (`traceparent`/`tracestate`), sem baggage; o corpo de negócio das mensagens não recebe campos de telemetria. Os logs das aplicações saem em JSON no stdout com os identificadores do span quando há contexto. **Emitir JSON não equivale a coletar/exportar logs ao Loki.**

Referências operacionais: [bootstrap Go](../../services/auth-service/telemetry.go), [bootstrap Python](../../services/analytics-service/telemetry.py), [produtor SQS](../../services/evaluation-service/sqs.go), [consumidor](../../services/analytics-service/app.py), [Collector](../../observability/otel-collector-local.yaml) e [overlay](../../docker-compose.otel.yaml).

## 3. Validações e rastreabilidade

### 3.1 Correspondência com o ensaio

Manifesto: [production-sha256-sql-final.json](qa-passos-locais-2026-10-27/production-sha256-sql-final.json). Os 28 arquivos abrangem código de produção, Dockerfiles, go.mod/go.sum e requirements dos cinco serviços. Recalculados em 2026-10-27 e 2026-10-28: **zero diferenças**. Isso preserva a pertinência da evidência anterior; não significa que todos os arquivos do repositório ou dependências remotas sejam imutáveis.

As três cópias de `telemetry.py` são idênticas por SHA-256; as duas de `telemetry.go` também. Os testes `telemetry_test.go` dos dois módulos Go são idênticos. Os testes Python de flag/targeting diferem apenas no nome do serviço; o corpo foi lido e a diferença foi comparada.

### 3.2 Integração e trace bruto

O [log final de integração](qa-passos-locais-2026-10-27/passo2-compose-sql-final.log) registra: saúde dos cinco serviços; rejeição de autenticação inválida; persistência de flags/regras; flags habilitadas/desabilitadas; regras 0%/100%; flag inexistente; cache e atualização após expiração; sete eventos persistidos e fila drenada. A etapa OTel adicional registra um evento controlado, JSON correlacionado, sanitização e ausência de spans de health.

O [resultado do trace](qa-passos-locais-2026-10-27/otel/resultado-traces.json) foi cruzado com `otel/traces.jsonl`, e não apenas aceito como resumo:

- **19 spans, cinco serviços**, IDs únicos, árvore sem ciclos e um pai externo.
- Um produtor SQS e um consumidor; o consumidor é filho do produtor.
- Spans CLIENT PostgreSQL: **auth 2, flag 1, targeting 1**.
- Presença dos spans de Redis, DynamoDB e confirmação da mensagem.
- Os logs do ensaio registram os cinco serviços com JSON correlacionado e os testes de sanitização aprovados.

A evidência anterior de 17 spans não é a aprovação vigente; o gate final passou a exigir SQL dos três serviços. Scripts de verificação: [test-flow.py](../../scripts/integration/test-flow.py), [test-traces.py](../../scripts/integration/test-traces.py) e [assert-events.py](../../scripts/integration/assert-events.py).

### 3.3 Suites existentes e limites

- Go: **13 testes principais + oito subtestes**, build/vet aprovados nos logs de `qa-otel-go-2026-10-27/`; auth tem cinco testes principais e evaluation oito. Parte da cobertura comum repete o bootstrap nos módulos independentes.
- Python: **20 testes** nas imagens de execução: flag 6, targeting 6, analytics 8. Logs: `tests-flag-service-sql-final-docker.log`, `tests-targeting-service-sql-final-docker.log` e `tests-analytics-service-sql-final-docker.log`, em `qa-passos-locais-2026-10-27/`.
- Nesta revisão, análise sintática AST dos **nove arquivos Python em services** aprovada, sem importá-los ou abrir clientes AWS.
- As suites não cobrem toda entrada inválida, falha de dependência, volume de carga, concorrência ou recuperação no Kubernetes. O teste de fallback abaixo cobre uma lacuna concreta, sem transformar os resultados anteriores em uma aprovação geral de resiliência.

## 4. Achados funcionais e implicações para a Fase 4

Os identificadores A-01 a A-04 são locais a este parecer; não substituem os IDs F/P/D do projeto. Estes achados são distintos das obrigações FIAP: o PDF não prescreve uma política específica de fallback, códigos HTTP de cada falha ou implementação de readiness.

### A-01 — Falha do targeting é tratada como ausência de regra

**Prioridade recomendada: alta antes de definir alerta e self-healing. Confirmado por código e sonda executada.**

Em `services/evaluation-service/evaluator.go:113`, qualquer `ruleErr` é apenas registrado; a função devolve `CombinedFlagInfo` com `Rule=nil`. Em `evaluator.go:258`, uma flag habilitada sem regra retorna `true`. A resposta termina em HTTP 200 (`handlers.go:63`) e a configuração degradada é gravada no cache (`evaluator.go:77`), cujo TTL é 30 segundos (`evaluator.go:24`). A distinção 404 feita em `fetchRule` não é respeitada pelo chamador: 401, 500 e timeout seguem o mesmo fallback.

| Caso da sonda | Resultado observado | Cache |
|---|---|---|
| Regra 404 | HTTP 200, `result=true` | `Rule:null` |
| Targeting 401 | HTTP 200, `result=true` | `Rule:null` |
| Targeting 500 | HTTP 200, `result=true` | `Rule:null` |
| Timeout targeting | HTTP 200, `result=true` | `Rule:null` |
| Flag 500 (controle) | HTTP 502 | Sem entrada |

Fonte da prova: [review_failure_test.go](qa-revisao-aplicacoes-2026-10-27/evaluation-failure/review_failure_test.go) e [targeting-failure-probe.log](qa-revisao-aplicacoes-2026-10-27/targeting-failure-probe.log), execução em **2026-10-27 22:32**. A sonda usou cópia exata dos fontes do evaluation, `httptest` e Redis em memória, sem AWS e sem alterar arquivos de produção. O PASS confirma a reprodução do comportamento atual, **não** aprova a política funcional.

O comportamento já existe na versão HEAD anterior à instrumentação: `git show HEAD:services/evaluation-service/evaluator.go` contém o mesmo desvio por `ruleErr` e a mesma liberação quando `Rule=nil`. Não é regressão introduzida pelo OTel.

**Impacto:** um alerta que monitore somente 5xx no evaluation pode não detectar a falha do targeting. Uma regra restritiva deixa de ser aplicada durante a indisponibilidade e a informação sem regra pode permanecer no cache até expirar. Para o cenário de demonstração, a falha deve produzir um sinal observável e a correção deve alterar esse sinal.

**Correção sugerida, não executada:** distinguir 404 de indisponibilidade/erro de autenticação; definir a política para erro de dependência (por exemplo, propagar erro ou usar configuração anterior conhecida); evitar cachear a ausência de regra inferida de uma falha. Criar regressões para 404, 401, 500, timeout e recuperação. Não atribuir à FIAP uma exigência de retornar especificamente 502 ou `false`.

Relação: manutenção funcional REQ-OBR-01 e desenho/demonstração REQ-OBR-16, 19, 28–31.

### A-02 — Falha de banco no auth aparece como credencial inválida

**Observação operacional confirmada por código e teste existente.** `services/auth-service/handlers.go:50–58` agrupa `sql.ErrNoRows`, cancelamento e outros erros de banco na mesma resposta 401. `handlers_test.go:46–50` simula erro arbitrário do driver e exige 401. Flag/targeting transformam qualquer resposta não 200 do auth em 401.

**Impacto:** uma indisponibilidade PostgreSQL pode aparecer como erro do cliente/autenticação; monitorar somente 5xx de auth não basta. O span SQL tem status de erro e pode fornecer um sinal complementar. Sugestão: separar chave inexistente de falha operacional e revisar o alerta usando esses sinais. Não executada; não é uma exigência específica de código HTTP do enunciado.

### A-03 — Health é prova de vida do servidor, não de funcionamento integral

Os endpoints retornam `status=ok` sem verificar dependências ou progresso da fila: auth `handlers.go:23`, evaluation `handlers.go:18`, flag `app.py:71`, targeting `app.py:68` e analytics `app.py:175`. O analytics responde health mesmo com SQS desabilitado, comportamento explicitamente permitido pelo modo local.

**Implicação:** a entrega precisa combinar a saúde do processo com requisição funcional, telemetria e consumo/persistência dos eventos. Não usar somente health/Pods Running como prova de REQ-OBR-01/23. Readiness mais precisa é uma sugestão técnica; acrescentar dependências indiscriminadamente à liveness também não é uma solução automática.

### A-04 — Reprodutibilidade das dependências ainda pode melhorar

`services/analytics-service/requirements.txt:1–2` não fixa Flask/Gunicorn; setuptools também não tem versão, e imagens-base Go/Python usam tags. Os builds existentes passaram; esta observação não afirma incompatibilidade atual. Recomenda-se registrar/estabilizar as versões efetivamente validadas antes da gravação final. A instrumentação OTel está fixada nos manifests de dependência; não concluir que todas as dependências do aplicativo estão fixadas.

## 5. Lacunas de entrega relacionadas a este escopo

| IDs | Situação encontrada | O que ainda precisa existir/comprovar |
|---|---|---|
| REQ-OBR-01 | Base funcional aprovada localmente; há o comportamento degradado A-01 | Ensaio funcional no destino de entrega e política de falha coerente com alertas/recuperação |
| REQ-OBR-02 | Cinco serviços conteinerizados; builds e integração locais comprovados | Preservar funcionamento após implantação e incluir prova na entrega |
| REQ-OBR-06–10 | Não implementados nesta composição | Stack de cluster/Helm, Prometheus, Loki, Grafana e dashboard; revisão GitOps complementa este parecer |
| REQ-OBR-11 | Parcial: Collector centraliza e sanitiza traces locais | Métricas + coleta/exportação de logs + backends corretos; o único pipeline atual é `traces` em `observability/otel-collector-local.yaml:56–60` |
| REQ-OBR-12 | New Relic escolhido no contexto; nenhuma integração operacional aqui | Conta/configuração e ingestão comprovada; não reabrir a escolha já registrada |
| REQ-OBR-13 | Implementado nos cinco serviços e comprovado localmente | Preservar instrumentação e suas variáveis ao implantar |
| REQ-OBR-14 | Propagação e trace completos localmente | Visualizar a requisição do evaluation no APM, conforme p. 4 |
| REQ-OBR-15 | Topologia local comprovada; Service Map externo não comprovado | Mostrar o mapa dos cinco serviços no APM; um trace com cache quente pode legitimamente envolver menos serviços |
| REQ-OBR-16–19/22 | Alertas, incidente, ChatOps e automação não existem nos arquivos deste escopo | Implementar integrações e provar o ciclo falha → detecção → acionamento → tentativa de correção |
| REQ-OBR-20 | Collector local não é stack IaC/GitOps entregue | Implantação declarativa da stack e Collector no repositório de entrega |
| REQ-OBR-21 | Código instrumentado presente no workspace local | Publicação autorizada do código e revisão do resultado entregue; esta auditoria não publicou nada |
| REQ-OBR-23/26–31/35–38 | Evidência local cobre parte do funcionamento | Evidências finais no cluster/APM/Grafana/Loki/ChatOps/automação, vídeo e prints no relatório |
| REQ-BON-02 | Bibliotecas OTel da linguagem adotadas | Preferência atendida localmente, sem promessa de pontuação extra |

A presença de pacotes `otel/metric` indiretos no go.mod não implementa SDK/exportação de métricas. O receptor OTLP do Collector também não cria automaticamente pipelines de métricas/logs. Nenhum exporter New Relic foi encontrado na configuração atual. As ausências dizem respeito ao código inspecionado; não são uma consulta às contas externas.

## 6. Inventário da leitura

Leitura funcional dos fontes e configurações, com cópias idênticas verificadas por hash/diff:

- `services/auth-service/`: `main.go`, `handlers.go`, `key.go`, `telemetry.go`, `handlers_test.go`, `telemetry_test.go`, `Dockerfile`, `go.mod`, `db/init.sql`; seção de observabilidade do README; `go.sum` verificado por hash como parte do manifesto.
- `services/evaluation-service/`: `main.go`, `handlers.go`, `evaluator.go`, `sqs.go`, `types.go`, `telemetry.go`, `evaluator_test.go`, `telemetry_test.go`, `Dockerfile`, `go.mod`; seção de observabilidade do README; `go.sum` verificado por hash.
- `services/flag-service/` e `services/targeting-service/`: `app.py`, `telemetry.py`, `tests/test_telemetry.py`, `Dockerfile`, `requirements.txt`, `db/init.sql`; seções de observabilidade/SQL do README.
- `services/analytics-service/`: `app.py`, `telemetry.py`, `tests/test_telemetry.py`, `Dockerfile`, `requirements.txt`; seção de observabilidade do README.
- `docker-compose.yaml`, `docker-compose.integration.yaml`, `docker-compose.otel.yaml`, `infra/postgres-app/01-init-multi-db.sh`.
- `observability/otel-collector-local.yaml` e `observability/README.md`.
- `scripts/test-compose.sh`, `scripts/test-observability.sh`, `scripts/integration/bootstrap-aws.py`, `assert-events.py`, `test-flow.py`, `test-traces.py`.
- Contexto e requisitos: LEIA-PRIMEIRO, trechos vigentes de PENDENCIAS/LOG e tabela dos 42 obrigatórios no README de requisitos.
- Evidências: manifesto de 28 fontes; JSON do trace e batches JSONL correspondentes; log integrado final; logs de testes Docker Python; testes/build/vet Go; relatório Go; sonda pontual A-01.

Esta revisão não é uma auditoria exaustiva de vulnerabilidades ou atualização de CVEs; não leu o código de todas as dependências externas, nem reanalisou integralmente as aulas. A aceitação dos requisitos é documental/funcional, com os limites acima. Não há alegação de CI remoto, produção AWS ou APM externos aprovados.

## 7. Handoff

O coordenador deve incorporar A-01 ao backlog técnico antes de escolher o cenário E4/E5, preservar A-02/A-03 como implicações para observabilidade e usar as evidências locais para marcar corretamente implementação versus comprovação externa. Não repetir a instrumentação ou importação. A prova local continua válida para seu escopo e os 28 hashes foram reconferidos em 2026-10-28.

Nenhum fonte operacional, material original, branch, commit, recurso cloud ou conta externa foi alterado por esta revisão. Novos arquivos limitam-se a este relatório e à sonda/cópia local em `qa-revisao-aplicacoes-2026-10-27/`, autorizada pelo coordenador para reproduzir o achado. LOG/PENDENCIAS centrais serão atualizados pelo coordenador para evitar escrita concorrente.
