# Instrumentação Go — verificação local 2026-10-27

TL;DR: auth-service e evaluation-service instrumentados; cinco testes auth e oito evaluation (mais quatro subtestes em cada serviço) aprovados, assim como gofmt, vet e build. Nenhum acesso AWS, Compose, commit, push ou PR executado por este agente.

Última atualização: 2026-10-27 10:55 (America/Sao_Paulo, UTC-03:00), Codex / go_otel_final.

## Checklist

- [x] Ler protocolo, P-008 e baseline aprovado de 2026-10-22.
- [x] Preservar fontes anteriores antes dos ajustes; hashes dos backups registrados.
- [x] Concluir bootstrap/middleware/logs e contexto SQL/Redis/HTTP/SQS.
- [x] Criar testes com receptor OTLP local, SQL/Redis simulados, HTTP local e fake SQS.
- [x] VERIFICAÇÃO: testes, gofmt, go vet, build e revisão do diff aprovados.
- [x] Entregar fontes estáveis ao coordenador para Docker Go 1.25 e integração dos cinco serviços.

## Resultado implementado

OTLP/HTTP opcional, habilitado somente por OTEL_EXPORTER_OTLP_ENDPOINT ou OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, respeitando OTEL_SDK_DISABLED; service.name configurável; SDK traces em batch. Sem exporters de métricas/logs. W3C TraceContext sem Baggage. Um middleware HTTP, exclusão de /health e eventos JSON estáticos no stdout com event/service.name/trace_id/span_id.

Auth: QueryRowContext herda o contexto HTTP. Spans SQL incluem sistema e operação, sem texto SQL, nome/chave/hash/parâmetros. Logs antigos com nome, fragmento de hash e erro de banco substituídos por eventos estáticos. Contratos HTTP e JSON preservados.

Evaluation: Redis GET/SET e chamadas HTTP paralelas herdam o contexto HTTP. Spans Redis sem chave/valor. Transporte otelhttp propaga W3C. Publicação SQS continua assíncrona e usa WithoutCancel + timeout próprio de cinco segundos, span PRODUCER e atributos traceparent/tracestate String. JSON EvaluationEvent mantém exatamente user_id/flag_name/result/timestamp. Encerramento: drenar HTTP → aguardar produtores → fechar clientes → flush/shutdown do SDK. Startup retorna erros para permitir defers; sinal normal não usa log.Fatal.

As bibliotecas HTTP podem produzir atributos URL antes do Collector; a allowlist e remoção de detalhes do Collector são responsabilidade da configuração integrada do coordenador. Nenhum exporter externo foi configurado aqui.

## Evidências e reprodução

Ambiente local em 2026-10-27: go1.27.1 windows/amd64. go.mod mantém go1.25.0; módulos OTel/sdk/exporter v1.46.0, otelhttp v0.71.0. go.mod das dependências principais/transitivas grpc v1.83.1 e x/net v0.58.0 conferidos: go1.25.0. Docker usa golang:1.25-alpine; o coordenador valida a imagem e o ensaio integrado separadamente.

Com GOCACHE/GOMODCACHE/GOPATH apontando para subpastas desta evidência:

```powershell
go -C services/auth-service test -count=1 -v ./...
go -C services/evaluation-service test -count=1 -v ./...
go -C services/auth-service vet ./...
go -C services/evaluation-service vet ./...
go -C services/auth-service build -o <qa>/auth-service-new.exe .
go -C services/evaluation-service build -o <qa>/evaluation-service-new.exe .
```

- auth-tests-final.log e evaluation-tests-final.log: testes aprovados; incluem OTLP HTTP protobuf base/TRACES_ENDPOINT, parent W3C, health excluído, SDK opt-in/disabled e JSON correlacionado; cancelamento SQL/Redis/HTTP; SQS após cancelamento, body preservado, produtor correto e erro sem detalhes sensíveis; drenagem de HTTP antes dos produtores.
- build-vet-result.json: quatro comandos (dois builds, dois vets) com saída 0; logs individuais *-build.log/*-vet.log.
- backup-sha256.json: fontes preservadas em ../../_ARQUIVO_MORTO/2026-10-27_instrumentacao-go/services/.
- production-sha256.json: hashes finais das fontes de produção. telemetry.go dos dois serviços: 9E6660343334E1CB11141096CEA331B367983D319EBD1D5E0700F456B1D75AAA. Última alteração real: 2026-10-27 10:50:49 UTC-03.
- tracked-diff-review.patch: diff dos arquivos rastreados. Arquivos novos revisados diretamente: telemetry.go, telemetry_test.go, handlers_test.go (auth), evaluator_test.go (evaluation).

Revisão do diff: lógica de percentuais, TTL, autorização, respostas e JSON de negócio mantidos; mudanças de comportamento intencionais são cancelamento das dependências com HTTP, prazo SQS de cinco segundos, logs sem dados de negócio e encerramento gracioso. Testes usam somente valores artificiais e serviços locais.

Fontes consultadas em 2026-10-27: https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@v0.71.0 ; https://pkg.go.dev/go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.46.0 ; https://pkg.go.dev/context#WithoutCancel ; fontes Go dos dois serviços e go.mod das dependências baixadas neste diretório.

## Handoff

Produção Go final e estável; não repetir a instrumentação. READMEs locais atualizados. O coordenador mantém o LOG/PENDENCIAS centrais e a evidência integrada; recebeu horário/hashes para conferir que a imagem Go testada reflete a última fonte. Sem New Relic ou AWS real nesta etapa. Revisão independente coordenada por auditoria_final; eventuais achados devem ser acrescidos sem apagar este registro.

## Revisão independente recebida — 2026-10-27

Codex / auditoria_final confirmou ao agente Go a leitura do helper listener final, testes SQS/cache/cancelamento, logs finais e build-vet-result.json. Parecer: aprovado, sem bloqueio concreto identificado. O revisor também recalculou o trace integrado do coordenador: 17 spans, cinco serviços, um PRODUCER e um CONSUMER com parentesco correto, sem ciclos e com pai externo único. A evidência integrada completa e a preservação final ficam no relatório do coordenador; este agente não executou Compose.
