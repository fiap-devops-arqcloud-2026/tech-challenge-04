# Revisao Python OpenTelemetry — 2026-10-27

TL;DR: revisao concluida e aprovada dos tres servicos Python, com 18 testes existentes e provas adicionais de isolamento SQS e ciclo de vida do SDK. Nenhuma alteracao de codigo foi necessaria. Rebuild e ensaio integrado Docker pertencem ao agente principal.

Ultima atualizacao: 2026-10-27 10:46 (America/Sao_Paulo, UTC-03:00), Codex, subagente python_otel_final. Horario aferido por Get-Date; timestamp completo em resultado-revisao.json.

## Escopo e lista de verificacao

- [x] Ler protocolo/P-008/LOG e evidencias de 2026-10-22; confirmar baseline funcional anterior registrado antes da instrumentacao.
- [x] Revisar app.py, telemetry.py, requisitos, Dockerfiles, testes e README dos tres servicos.
- [x] Reexecutar baseline Python: flag 5/5, targeting 5/5, analytics 8/8.
- [x] Provar isolamento de contexto por mensagem, restauracao do contexto ambiente e comportamento com exportador com falha.
- [x] Conferir compilacao, lint fatal do CI, dependencias e diff.
- [x] Registrar resultado, limites e estado exato para o principal.

Evidencias locais ignoradas: `00_COLAB_IA/02_TRABALHO/qa-otel-python-2026-10-27/`. Ambiente reutilizado: `.venv` de `otel-python-2026-10-22_v01`, Python 3.12.14 confirmado em 2026-10-27. Nenhum teste desta revisao acessa rede ou AWS. Nao executar Compose neste subagente; nao alterar Git, contexto compartilhado, Terraform ou servicos de outros agentes.

## Conclusoes da revisao

1. Os 18 testes existentes passam novamente. Os testes usam SERVICE explicito em cada servico, inclusive analytics em `/app`; o erro de inferencia de diretorio de 2026-10-22 ja foi corrigido no fonte. O principal precisa rebuildar para que as imagens contenham esses testes.
2. Nao existe falha de contexto padrao em `message_context`: o SDK fixado cria `Context()` vazio em `TraceContextTextMapPropagator.extract` quando `context=None`. Nao acrescentar codigo redundante apenas por essa suspeita. A prova adicional na pasta de QA confirmou cinco mensagens consecutivas, com atributos ausentes, vazios, traceparent invalido, StringValue de tipo invalido e pai W3C valido: nenhum caso herdou o span ambiente por engano ou vazou o span consumidor para o chamador.
3. Os tres telemetry.py possuem o mesmo SHA-256 `A13F2A8564C931A3C7586E888DC3B46D695A62D70EE3BF73361FA29FDEDA2917`. A duplicacao e intencional por contexto Docker independente.
4. O SDK TracerProvider registra `shutdown` em atexit por padrao; o Dockerfile usa `exec gunicorn` e nao usa preload. Nao ha flush por requisicao. Fonte: SDK 1.45.1 instalado e Dockerfiles locais, lidos em 2026-10-27.

## Verificacoes de 2026-10-27

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

Nenhum arquivo em `services/` foi alterado nesta revisao; portanto, nao houve necessidade de preservar novas versoes desses fontes. A instrumentacao de 2026-10-22, o manifesto anterior e suas copias permanecem intactos. O rascunho desta nota foi copiado antes da consolidacao para `00_COLAB_IA/_ARQUIVO_MORTO/2026-10-27_instrumentacao-python/02_TRABALHO/REVISAO_PYTHON_OTEL_2026-10-27_rascunho_v01.md`; esta nota v01 e a versao vigente. Arquivos novos: esta nota e as evidencias ignoradas do QA. Nenhuma escrita no contexto compartilhado ou nos escopos de outros agentes.

## Limites e estado para o proximo agente

- O SDK trata erro de exportacao em segundo plano e preservou a resposta HTTP na prova; seu logger interno escreveu o erro esperado no stderr. JSON e sanitizacao prometidos pelo aplicativo nao se estendem aos logs internos do SDK/Gunicorn. O erro da prova e sintetico e nao contem dado real.
- Os instrumentadores automaticos podem produzir URL completa, SQL/DSN e detalhes de excecao antes do Collector. Os logs controlados do aplicativo nao incluem esses dados; o Collector e a fronteira de sanitizacao antes da persistencia de spans. Nao apontar diretamente para exporter externo sem rever essa politica.
- Warnings de deprecacao Flask/Werkzeug herdados e de comentarios nosec do Bandit aparecem; nao representam falha dos testes nem achado medio/alto. Nao atualizar frameworks de negocio neste escopo.
- A prova de lifecycle confirma force_flush/shutdown em processo, sem afirmar encerramento real via SIGTERM ou resistencia a SIGKILL. A configuracao atual sem preload e atexit foi inspecionada; o ensaio Linux do principal complementa este resultado.
- Proximo passo P-008: principal rebuilda as tres imagens Python para incluir SERVICE explicito nos testes, executa os testes nas imagens e fecha o ensaio funcional + OTLP/Collector com os cinco servicos. Estes testes locais nao comprovam exportacao externa, AWS, CI remoto ou conclusao da Fase 4.

Fontes da revisao, lidas em 2026-10-27: app.py, telemetry.py, requirements.txt, Dockerfile, README.md e tests/test_telemetry.py dos tres servicos; SDK instalado `opentelemetry/trace/propagation/tracecontext.py`, `opentelemetry/sdk/trace/__init__.py`, `opentelemetry/sdk/_shared_internal/__init__.py`; overlay/Collector e scripts de integracao apenas em leitura; protocolo/P-008/LOG vigentes. O resultado foi comunicado ao principal e ao revisor independente; nao executar commit/push/PR/main/AWSreal.

