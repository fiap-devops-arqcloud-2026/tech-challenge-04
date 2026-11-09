# Revisao independente de Terraform e observabilidade local

TL;DR: as principais afirmacoes do relatorio Terraform de 2026-10-22 continuam compativeis com o checkout lido em 2026-10-27. A revisao estatica do Collector, dos testes de integracao e dos fontes Go/Python nao identificou falha concreta bloqueante no escopo. Os testes unitarios atuais dos agentes Go/Python possuem evidencias aprovadas; o ensaio Docker/Collector atual e seu encerramento pertencem ao agente principal. Nenhuma evidencia local comprova AWS, cluster, New Relic ou CI remoto.

**Estado vigente, 2026-10-27 11:05 (UTC-03:00): aprovado apos corrigir e testar a ausencia dos spans SQL Python. Nova prova: 19 spans, cinco servicos, SQL CLIENT em auth/flag/targeting e vinte testes Python nas imagens. Ler o encerramento ao final; os cortes anteriores foram preservados como historico da revisao.**

Ultima atualizacao: 2026-10-27 10:53 (America/Sao_Paulo, UTC-03:00), Codex, subagente auditoria_final. Horario obtido por Get-Date durante a revisao. Fontes e resultados abaixo referem-se a leitura de 2026-10-27, exceto quando outra data esta expressa.

## Escopo e verificacao

- [x] Ler protocolo vigente, P-008, topo do LOG e D-016.
- [x] Confrontar relatorio Terraform com inventario, backends, providers, variaveis, remote_state, lockfiles e workflow.
- [x] Conferir links locais do relatorio e existencia dos nomes locais de configuracao, sem abrir state, cache ou credenciais.
- [x] Revisar Collector/overlay, script Bash e teste de traces.
- [x] Revisar fontes Go/Python consolidados e evidencias dos agentes responsaveis.
- [x] Executar verificacoes proprias sem efeito sobre fontes: sintaxe Bash, AST Python e diff check dos caminhos pertinentes.
- [x] Registrar limites de evidencia e passos restantes para P-008.

Este agente nao executou Docker, Terraform, AWS, alteracao Git ou varredura de seguranca. Criou somente este relatorio. A finalizacao de LOG/PENDENCIAS/DOSSIE cabe ao principal, sem sobrescrever os registros de outros agentes.

## Terraform: resultado da conferencia

O relatorio [Terraform/backend de 2026-10-22](RELATORIO_TERRAFORM_BACKEND_2026-10-22_v01.md) e adequado para explicar do simples ao tecnico. Distingue a planta (`.tf`), o cadastro do que Terraform gerencia (state), o lugar e mecanismo desse cadastro (backend), a proposta (plan) e a execucao (apply). Importar codigo nao importa os objetos da conta anterior.

| Afirmacao | Conferencia em 2026-10-27 | Fonte local |
|---|---|---|
| Inventario proprio | 40 arquivos `.tf`; 7 diretorios de modulos locais; 8 chamadas `module`; 51 blocos `resource`; 13 blocos `data` | Enumeracao `terraform/**`, excluindo `.terraform/`, e busca das declaracoes |
| Tres raizes e estados | Base, cluster e k8s; chaves `phase4/prod/base.tfstate`, `phase4/prod/cluster.tfstate` e `phase4/prod/k8s.tfstate` | `terraform/backend.tf`, `cluster/backend.tf`, `k8s/backend.tf` |
| Backend parcial | As tres raizes fixam chave, `encrypt=true` e `use_lockfile=true`; bucket/regiao dependem da configuracao local | Mesmos backends e tres `backend.hcl.example` |
| Arquivos reais nesses nomes | `backend.hcl`, `terraform.tfvars`, `terraform.tfstate` e `tfplan` ausentes nas tres raizes; `.terraform/` e `.terraform.lock.hcl` presentes | Somente Test-Path; conteudo de cache/state nao inspecionado |
| Leitura entre camadas | Cluster le base; k8s le base e cluster, usando bucket/regiao/chaves proprios das variaveis | `terraform/cluster/data.tf`, `terraform/k8s/data.tf` |
| Protecao de conta | `expected_aws_account_id` obrigatorio e validado; `allowed_account_ids` no provider AWS de cada raiz | Tres `providers.tf` e `variables.tf` |
| CI Terraform | Instala Terraform 1.16.0 e faz fmt/init sem backend/validate nas tres raizes; sem plan/apply | `.github/workflows/terraform-check.yml` |
| Links do relatorio | 64 links locais com arquivos existentes e linhas dentro dos arquivos; 0 falhas | Verificador PowerShell desta revisao |

As contagens sao de declaracoes, nao de instancias ativas ou de um plano. A conta, o bucket e recursos remotos efetivamente existentes continuam **[INCERTO]**: nao foram consultados AWS, credenciais, variaveis de ambiente, backend real ou estados. A ausencia dos nomes locais citados nao elimina a possibilidade de configuracao externa.

O relatorio explica corretamente tres limites relevantes: variaveis Terraform nao preenchem automaticamente o backend; o guard do provider nao se estende automaticamente ao backend/remote_state/exec AWS CLI; e `sensitive` nao remove segredos do state. Tambem registra a divergencia entre o comentario historico sobre `use_lockfile` e a documentacao consultada em 2026-10-22, sem altera-la silenciosamente. Nao foi repetida nesta revisao a consulta web de 2026-10-22 nem a validacao Terraform de 2026-10-20.

## Collector e teste de ponta a ponta local

Fontes: `docker-compose.otel.yaml`, `observability/otel-collector-local.yaml`, `observability/README.md`, `scripts/test-observability.sh` e `scripts/integration/test-traces.py`.

- O overlay fornece endpoint OTLP/HTTP e nomes distintos aos cinco servicos. Collector fixado em versao e digest; diagnostico publicado em loopback; saida debug basica/arquivo, sem exporter ou chave New Relic.
- A pipeline aplica memory_limiter, filtro de health, transformacao por lista permitida e batch antes das duas saidas. Atributos comuns com URL completa, query, headers, SQL/DSN, identificadores e payload nao sao mantidos; mensagens de status e detalhes das excecoes sao removidos. `error.type` e `exception.type` permanecem.
- O teste verifica a extensao health do Collector, cria uma requisicao de avaliacao com pai W3C conhecido e aguarda os cinco service.name e todos os pais esperados. Isso evita aceitar apenas o consumidor que tenha chegado antes do produtor em outro lote.
- Exige um PRODUCER e um CONSUMER, associa o pai do consumidor ao span produtor, rejeita span IDs duplicados e pais ausentes, verifica duracoes e uma unica instrumentacao SERVER da avaliacao. A persistencia e confirmada pelo worker real no simulador; a resposta funcional e comparada ao contrato esperado.
- Logs JSON devem conter o trace_id controlado e span_id em todos os cinco servicos, sem a credencial gerada. A sonda OTLP sintetica inclui URL/query/header/SQL/identificador e detalhes de erro para comprovar a sanitizacao da saida quando executada; /health e verificado separadamente.

O teste integrado do principal ainda precisa ser executado com as imagens atuais para transformar essa cobertura de codigo em evidencia de execucao atual. A lista permitida opera sobre atributos; nomes de spans e campos permitidos precisam continuar controlados, conforme o README. Auto instrumentadores podem produzir dados detalhados antes do Collector. Logs internos do SDK/Gunicorn nao possuem a mesma garantia de formato e sanitizacao dos eventos controlados da aplicacao.

## Revisao dos servicos e evidencias atuais

Go: fontes auth/evaluation, helpers de telemetria e testes foram lidos apos a consolidacao. Handler e clientes HTTP transportam contexto; SQL/Redis possuem spans sem parametros de negocio; o produtor SQS conserva o contexto com `WithoutCancel` e prazo proprio de 5s. A drenagem aguarda handlers antes dos produtores e shutdown do SDK. W3C vai em MessageAttributes; o JSON de negocio conserva `user_id`, `flag_name`, `result`, `timestamp`.

Os logs finais de 2026-10-27 fornecidos pelo agente Go foram abertos: auth tem 5 testes principais aprovados e evaluation 8, com quatro subtestes em cada servico. Incluem receptor OTLP HTTP/protobuf, endpoints base/especifico, pai HTTP, exclusao health, opt-in/desativacao, cancelamento, ordem de drenagem, cache e corpo/contexto SQS. Fontes: `qa-otel-go-2026-10-27/auth-tests-final.log`, `evaluation-tests-final.log` e testes dos dois servicos. O agente tambem informou go vet aprovado; este revisor nao o reexecutou.

Python: fontes dos tres servicos e testes foram lidos. A mudanca preserva persistir antes de confirmar a mensagem; erros nao confirmam a mensagem. Mensagens de negocio/credenciais nao sao interpoladas nos logs controlados. Os tres `telemetry.py` possuem o mesmo SHA-256, reconferido por este agente. Os testes unitarios cobrem HTTP/contexto/logs, health, opt-in e falhas do consumidor.

O [relatorio Python de 2026-10-27](REVISAO_PYTHON_OTEL_2026-10-27_v01.md) e `qa-otel-python-2026-10-27/resultado-revisao.json` foram abertos: 18/18 testes aprovados, cinco casos adicionais de contexto SQS e provas de sucesso/falha do exporter com fechamento. Sao execucoes do agente Python, nao repeticoes por este revisor; o limite de nao equivalerem a SIGTERM real/exportacao OTLP real esta explicito nessa evidencia.

Verificacoes executadas por este revisor em 2026-10-27: `bash -n scripts/test-observability.sh` saida 0; AST de 10 arquivos Python (nove em services e test-traces.py) aprovado, sem importar as aplicacoes; `git diff --check` dos caminhos de servicos/testes/overlay/observability saida 0. Warnings Git de conversao futura LF/CRLF apareceram, sem erro de whitespace. Arquivos ainda nao rastreados foram lidos diretamente; diff check sozinho nao os valida.

## Estado para o principal e proximo agente

Nao identifiquei achado concreto P1/P2 que bloqueie o ensaio local no escopo revisado. Esse parecer e uma revisao de codigo/evidencias, nao uma certificacao de seguranca ou de ausencia de falhas.

P-008 ainda requer do principal: rebuild e testes nas imagens atuais; execucao integrada de negocio e traces; leitura do resultado exportado para confirmar os cinco servicos/parentage/sanitizacao; relatorio do passo2 com data e fonte; limpeza apenas do laboratorio autorizado e atualizacao do handoff. O passo1 de sete eventos e a validacao Terraform anteriores conservam suas datas originais; nao foram reexecutados por este agente em 2026-10-27.

Continuam separados: validacao local versus ingestao New Relic, implementacao Kubernetes/stack completa, AWS real, publicacao de imagens, CI remoto e entrega da Fase 4. Nao houve commit/push/PR/main, leitura de segredos ou alteracao da fonte Fase 3 por esta revisao.

## Consolidacao final — 2026-10-27 10:55 (America/Sao_Paulo, UTC-03:00)

Este complemento preserva o corte anterior e atualiza os pontos que ainda aguardavam evidencia. O principal informou ensaio Docker concluido as 10:52, saida 0. Este revisor abriu `qa-passos-locais-2026-10-27/passo2-compose.log` e `qa-passos-locais-2026-10-27/otel/resultado-traces.json`: o log registra aprovacao dos cinco health checks, autenticacao, regras/persistencia/cache/TTL, sete eventos funcionais mais um evento controlado, fila drenada, logs correlacionados nos cinco servicos, sonda de sanitizacao e exclusao dos probes health.

Uma verificacao propria, somente em memoria, recalculou a topologia a partir do resultado exportado: **17 spans, cinco servicos, IDs unicos, um produtor, um consumidor e pai do consumidor igual ao span produtor**. Cada cadeia foi percorrida ate o mesmo pai externo; nao ha ciclo nem pai interno ausente. Essa e revisao independente de evidencia produzida pelo principal, sem reexecucao de Docker por este agente.

Os checks `http_sqs_parentage`, `business_contract`, `privacy_probe` e `health_exclusion` estao aprovados no JSON, em concordancia com o log. O log mostra os testes executando os dois contratos, e a sonda inclui dados sinteticos; nenhuma credencial real foi lida por esta revisao. O principal informou tambem 18 testes Python aprovados nas imagens reconstruidas.

O artefato Go `qa-otel-go-2026-10-27/build-vet-result.json` foi aberto e registra build/vet com saida 0 para auth e evaluation. Os arquivos finais do overlay, Collector e script foram relidos; o script inclui a preservacao do caminho Linux no Git Bash com `MSYS_NO_PATHCONV=1`, e `bash -n` foi conferido novamente apos essa mudanca.

**Parecer final do escopo revisado:** aprovado, sem falha concreta bloqueante identificada. O ensaio atual cobre a integracao local dos cinco servicos e sanitizacao de traces; nao afirma ingestao New Relic, coleta de logs/metricas no cluster ou requisitos posteriores da Fase 4. Restam ao principal apenas consolidar os relatorios/contexto e encerrar/conferir os recursos descartaveis exclusivos do laboratorio, conforme P-008. As validacoes antigas mantem suas datas originais; o novo ensaio local e de 2026-10-27.

## Reabertura do parecer — 2026-10-27 10:56 (America/Sao_Paulo, UTC-03:00)

**O parecer de aprovacao acima fica suspenso ate nova evidencia.** A conferencia propria da arvore de 17 spans continua correta, mas o principal identificou uma lacuna que esta revisao nao havia exigido: faltam spans SQL de flag-service e targeting-service. O JSON exportado mostra PostgreSQL somente em auth; os cinco servicos estarem conectados por HTTP/SQS nao comprova todas as dependencias prometidas.

Achado P2 desta revisao: `scripts/integration/test-traces.py:167` aceita a arvore quando tem todos os servicos, PRODUCER/CONSUMER, SERVER evaluation e DynamoDB, sem exigir SQL nos dois servicos Python. Assim, a aprovacao desse teste nao detecta a perda da instrumentacao psycopg2. Em 2026-10-27, `telemetry.py` instala Psycopg2Instrumentor, mas as aplicacoes usam `cursor_factory=RealDictCursor`; a causa exata permanece **[INCERTO]**, em investigacao pelo agente Python. Nao declarar suporte SQL desses dois servicos como comprovado.

Proxima verificacao: aguardar a correcao do principal/agente responsavel; conferir fonte e teste de regressao do caminho RealDictCursor; exigir spans CLIENT PostgreSQL nos dois servicos no teste integrado; reabrir o novo JSON/log e recalcular a arvore antes de emitir novo parecer. Nenhuma fonte ou teste foi alterado por este revisor.

## Encerramento do achado SQL e parecer vigente — 2026-10-27 11:05 (America/Sao_Paulo, UTC-03:00)

**Achado P2 resolvido; parecer reemitido como aprovado.** O agente Python confirmou a causa no SDK fixado: a factory de cursor passada explicitamente em `conn.cursor(cursor_factory=RealDictCursor)` substituia a factory envolvida pelo instrumentador. A correcao define RealDictCursor na criacao do pool/conexao e usa `conn.cursor()` nos endpoints. As respostas por dicionario e os parametros SQL permanecem preservados.

Este revisor leu a correcao nos dois app.py e a regressao em seus testes. O teste importa a aplicacao real e usa o instrumentador/pool reais, com conexao/execucao substituidas localmente, para exigir SELECT CLIENT filho do SERVER Flask, resposta dict e ausencia do parametro privado nos atributos. Os logs finais abertos registram 6 testes flag, 6 targeting e 8 analytics aprovados. O agente Python tambem documentou a prova vermelha contra os fontes anteriores. Fonte consolidada: [revisao Python](REVISAO_PYTHON_OTEL_2026-10-27_v01.md) e `qa-otel-python-2026-10-27/resultado-revisao-sql-final.json`. O JSON anterior de 18 testes e historico. O QA Windows usou psycopg2-binary 2.9.11; o runtime manteve o pin 2.9.5 e foi complementado pela prova Docker abaixo.

O teste integrado passou a exigir CLIENT PostgreSQL nos tres servicos `auth-service`, `flag-service`, `targeting-service`, reconhecendo `db.system` e `db.system.name`, e registra `postgresql_client_spans` no JSON. Isso fecha a lacuna que permitira aceitar a arvore de 17 spans sem os dois SQL Python. O total de spans nao foi fixado no gate.

Este revisor abriu a **nova** evidencia `qa-passos-locais-2026-10-27/passo2-compose-sql-final.log`, `otel/resultado-traces.json` e o arquivo de traces sanitizados. Recalculou, sem executar Docker:

- 19 spans, cinco servicos, IDs unicos, uma arvore aciclica chegando ao mesmo pai externo.
- Um PRODUCER e um CONSUMER; pai do consumidor igual ao span produtor.
- Quatro CLIENT PostgreSQL: dois auth, um flag e um targeting; **cada SQL e filho de um SERVER do mesmo servico**.
- Log com sete eventos funcionais mais um controlado persistidos e fila drenada; gate SQL tres servicos, logs correlacionados nos cinco, sonda de sanitizacao e health todos aprovados.

Tambem abriu os tres logs `tests-*-sql-final-docker.log` produzidos pelo principal: **6 + 6 + 8 = 20 testes aprovados nas imagens reconstruidas**. Estes resultados atuais substituem a prova anterior de 18 testes e a exportacao de 17 spans para o fechamento do passo2. As datas e limitacoes das validacoes Terraform e do passo1 originais continuam preservadas.

Nao resta bloqueio concreto no codigo/evidencia revisados para esse passo local. O principal encerra a documentacao e os recursos exclusivos do laboratorio e registra o handoff. Este parecer nao comprova New Relic, AWS/cluster, CI remoto ou a stack de logs/metricas da Fase 4; nenhum desses ambientes foi acessado por este revisor.
