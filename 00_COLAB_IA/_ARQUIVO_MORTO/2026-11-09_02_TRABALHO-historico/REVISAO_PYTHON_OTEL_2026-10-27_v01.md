# Revisao Python OpenTelemetry — 2026-10-27

TL;DR: revisao Python concluida apos corrigir ausencia dos spans SQL de flag/targeting: RealDictCursor passou para a criacao do pool/conexao. Vinte testes finais aprovados (6 flag, 6 targeting, 8 analytics), com regressao que falha nos fontes anteriores. Provas adicionais SQS/SDK permanecem aprovadas. Rebuild e ensaio integrado Docker/Collector pertencem ao agente principal.

Ultima atualizacao: 2026-10-27 11:03 (America/Sao_Paulo, UTC-03:00), Codex, subagente python_otel_final. Horario aferido por Get-Date; corte final em resultado-revisao-sql-final.json. O JSON resultado-revisao.json preserva a rodada anterior de 10:46, com 18 testes e sem edicoes, e nao e o resultado final.

## Escopo e lista de verificacao

- [x] Ler protocolo/P-008/LOG e evidencias de 2026-10-22; confirmar baseline funcional anterior registrado antes da instrumentacao.
- [x] Revisar app.py, telemetry.py, requisitos, Dockerfiles, testes e README dos tres servicos.
- [x] Reexecutar baseline Python: flag 5/5, targeting 5/5, analytics 8/8.
- [x] Provar isolamento de contexto por mensagem, restauracao do contexto ambiente e comportamento com exportador com falha.
- [x] Conferir compilacao, lint fatal do CI, dependencias e diff.
- [x] Registrar resultado, limites e estado exato para o principal.

Evidencias locais ignoradas: `00_COLAB_IA/02_TRABALHO/qa-otel-python-2026-10-27/`. Ambiente reutilizado: `.venv` de `otel-python-2026-10-22_v01`, Python 3.12.14 confirmado em 2026-10-27. Nenhum teste desta revisao acessa rede ou AWS. Nao executar Compose neste subagente; nao alterar Git, contexto compartilhado, Terraform ou servicos de outros agentes.

## Primeira rodada da revisao — 2026-10-27 10:46

1. Os 18 testes existentes passam novamente. Os testes usam SERVICE explicito em cada servico, inclusive analytics em `/app`; o erro de inferencia de diretorio de 2026-10-22 ja foi corrigido no fonte. O principal precisa rebuildar para que as imagens contenham esses testes.
2. Nao existe falha de contexto padrao em `message_context`: o SDK fixado cria `Context()` vazio em `TraceContextTextMapPropagator.extract` quando `context=None`. Nao acrescentar codigo redundante apenas por essa suspeita. A prova adicional na pasta de QA confirmou cinco mensagens consecutivas, com atributos ausentes, vazios, traceparent invalido, StringValue de tipo invalido e pai W3C valido: nenhum caso herdou o span ambiente por engano ou vazou o span consumidor para o chamador.
3. Os tres telemetry.py possuem o mesmo SHA-256 `A13F2A8564C931A3C7586E888DC3B46D695A62D70EE3BF73361FA29FDEDA2917`. A duplicacao e intencional por contexto Docker independente.
4. O SDK TracerProvider registra `shutdown` em atexit por padrao; o Dockerfile usa `exec gunicorn` e nao usa preload. Nao ha flush por requisicao. Fonte: SDK 1.45.1 instalado e Dockerfiles locais, lidos em 2026-10-27.

## Verificacoes da primeira rodada de 2026-10-27

| Verificacao | Resultado | Evidencia na pasta QA |
|---|---|---|
| Testes flag | 5/5 | tests-flag-service-baseline.log |
| Testes targeting | 5/5 | tests-targeting-service-baseline.log |
| Testes analytics | 8/8 | tests-analytics-service-baseline.log |
| Isolamento SQS e restauracao de contexto | 5 casos aprovados | probe-context.log |
| Exportador em lote e shutdown | sucesso aprovado | probe-export-success.log |
| Excecao no exportador | resposta HTTP 200 preservada e shutdown concluido | probe-export-failure.log |
| compileall dos tres servicos | aprovado | resultado-revisao.json e pycache local |
| Flake8 fatal, selecao E9/F63/F7/F82 do CI | 0 erros | flake8.log |
| pip check | dependencias coerentes | pip-check.log |
| Bandit -ll | 0 medio/alto | bandit.json |
| git diff --check, somente servicos Python | aprovado | resultado-revisao.json |
| Versoes efetivamente instaladas | SDK/API/exporter 1.45.1; instrumentadores 0.66b1 | versions.json |

As provas extras usam os instrumentadores/SDK reais e exportador substituto em memoria, sem requisicoes de rede. `provider.force_flush()` foi usado apenas no QA para tornar a verificacao deterministica. A aplicacao continua sem flush por request.

## Preservacao e de-para

Na primeira rodada, nenhum arquivo em `services/` foi alterado. A reabertura SQL descrita abaixo alterou seis arquivos e possui copias verificadas antes da edicao. A instrumentacao/documentacao de 2026-10-22, o manifesto anterior e suas copias permanecem intactos. O rascunho desta nota foi copiado antes da consolidacao para `00_COLAB_IA/_ARQUIVO_MORTO/2026-10-27_instrumentacao-python/02_TRABALHO/REVISAO_PYTHON_OTEL_2026-10-27_rascunho_v01.md`; o texto anterior a reabertura foi preservado como `REVISAO_PYTHON_OTEL_2026-10-27_antes-sql_v01.md` na mesma pasta. Esta nota v01 e a versao vigente. Nenhuma escrita no contexto compartilhado ou nos escopos de outros agentes.

## Limites e estado para o proximo agente

- O SDK trata erro de exportacao em segundo plano e preservou a resposta HTTP na prova; seu logger interno escreveu o erro esperado no stderr. JSON e sanitizacao prometidos pelo aplicativo nao se estendem aos logs internos do SDK/Gunicorn. O erro da prova e sintetico e nao contem dado real.
- Os instrumentadores automaticos podem produzir URL completa, SQL/DSN e detalhes de excecao antes do Collector. Os logs controlados do aplicativo nao incluem esses dados; o Collector e a fronteira de sanitizacao antes da persistencia de spans. Nao apontar diretamente para exporter externo sem rever essa politica.
- Warnings de deprecacao Flask/Werkzeug herdados e de comentarios nosec do Bandit aparecem; nao representam falha dos testes nem achado medio/alto. Nao atualizar frameworks de negocio neste escopo.
- A prova de lifecycle confirma force_flush/shutdown em processo, sem afirmar encerramento real via SIGTERM ou resistencia a SIGKILL. A configuracao atual sem preload e atexit foi inspecionada; o ensaio Linux do principal complementa este resultado.
- Proximo passo P-008: principal rebuilda as tres imagens Python para incluir SERVICE explicito nos testes, executa os testes nas imagens e fecha o ensaio funcional + OTLP/Collector com os cinco servicos. Estes testes locais nao comprovam exportacao externa, AWS, CI remoto ou conclusao da Fase 4.

Fontes da revisao, lidas em 2026-10-27: app.py, telemetry.py, requirements.txt, Dockerfile, README.md e tests/test_telemetry.py dos tres servicos; SDK instalado `opentelemetry/trace/propagation/tracecontext.py`, `opentelemetry/sdk/trace/__init__.py`, `opentelemetry/sdk/_shared_internal/__init__.py`; overlay/Collector e scripts de integracao apenas em leitura; protocolo/P-008/LOG vigentes. O resultado foi comunicado ao principal e ao revisor independente; nao executar commit/push/PR/main/AWSreal.

## Reabertura e correcao SQL — resultado final em 2026-10-27 11:03

O principal identificou uma lacuna real no trace integrado anterior: a arvore tinha os cinco servicos e 17 spans, porem nao continha spans PostgreSQL dos servicos Python. A aprovacao anterior baseada nos 18 testes nao comprovava a instrumentacao dos cursores reais. O principal suspendeu a aprovacao, preservou o corte anterior e liberou a correcao depois que a execucao em curso terminou.

Causa confirmada no Psycopg2Instrumentor 0.66b1: `DatabaseApiIntegration.wrapped_connection` configura a factory instrumentada em `psycopg2.connect`. As chamadas `conn.cursor(cursor_factory=RealDictCursor)` sobrescreviam essa factory e chamavam execute sem o wrapper de tracing.

Correcao minima em flag e targeting: `SimpleConnectionPool(..., cursor_factory=RealDictCursor)` define a factory base antes de connect ser envolvido; os endpoints usam `conn.cursor()`. A factory instrumentada e subclasse de RealDictCursor, preservando linhas em dicionario. SQL, parametros, transacoes, respostas e `capture_parameters=False`/SQLCommenter desligado foram mantidos. O cursor de DELETE de flag passa a usar o mesmo padrao; ele so usa rowcount, sem alterar o contrato de resposta. Analytics/telemetry/requirements/Dockerfiles nao receberam alteracoes nesta reabertura.

Foi acrescentado um teste em cada servico. Ele usa Flask, SimpleConnectionPool, RealDictCursor e Psycopg2Instrumentor reais, substituindo apenas a conexao/execute/fetchone por objetos locais sem rede. Exige a mesma resposta JSON em dicionario, um SELECT CLIENT filho do SERVER Flask, parametros enviados intactos e valores privados ausentes dos atributos SQL, sem SQLcomment. A sonda `probe-sql-regression-red.py` executou o teste novo contra cada app.py preservado antes da correcao: ambos falharam exatamente porque a contagem SELECT era 0 em vez de 1. O teste passa contra o app.py corrigido. Os logs red contêm FAIL deliberado e a sonda retorna 0 apenas quando demonstra essa falha esperada; nao sao falhas pendentes.

| Verificacao final apos a correcao | Resultado | Evidencia em qa-otel-python-2026-10-27 |
|---|---|---|
| Testes flag | 6/6 | tests-flag-service-final.log |
| Testes targeting | 6/6 | tests-targeting-service-final.log |
| Testes analytics | 8/8 | tests-analytics-service-final.log |
| Total Python | 20/20 | resultado-revisao-sql-final.json |
| Regressao no fonte antigo | falha SELECT 0 != 1 demonstrada nos dois | red-flag-service.log; red-targeting-service.log |
| compileall e Flake8 fatal | aprovados, 0 erros | flake8-final.log; resultado-revisao-sql-final.json |
| pip check e diff check | aprovados | pip-check-final.log; resultado-revisao-sql-final.json |
| Bandit -ll | 0 medio/alto | bandit-final.json |
| Backups e hashes antes/depois | seis arquivos preservados e SHA conferido | preservacao-sql-cursor.json; resultado-revisao-sql-final.json |

Ambiente da prova Windows: a venv anterior nao continha psycopg2 porque os testes antigos nao exercitavam esse caminho. Foi instalado **psycopg2-binary 2.9.11 somente nessa venv de QA** com Python 3.12, sem alterar requirements. Os servicos/Docker continuam fixados em **psycopg2-binary 2.9.5**; somente o ensaio Docker do principal comprovara essa versao runtime e a operacao PostgreSQL real. Pip e o teste local nao substituem essa prova.

De-para: app.py, tests/test_telemetry.py e README.md de flag-service/targeting-service foram copiados antes da edicao para `00_COLAB_IA/_ARQUIVO_MORTO/2026-10-27_instrumentacao-python/sql-cursor/services/<servico>/`. O manifesto registra os seis SHA anteriores e finais. READMEs receberam nota de 2026-10-27 sobre factory/teste, preservando a documentacao anterior. Nenhum arquivo da versao documental de 2026-10-22 foi regravado.

Estado para o proximo agente: fontes estabilizados e principal/revisor avisados. O principal deve rebuildar flag/targeting com os testes atuais e executar seu gate integrado exigindo CLIENT PostgreSQL em auth, flag e targeting. A expectativa de dois spans adicionais decorre dos dois SELECT antes ausentes; nao registrar quantidade integrada final ate o ensaio real concluir. Nao executar novas edicoes nos servicos durante esse build; manter ausencia de push/commit/PR/main/AWSreal.

