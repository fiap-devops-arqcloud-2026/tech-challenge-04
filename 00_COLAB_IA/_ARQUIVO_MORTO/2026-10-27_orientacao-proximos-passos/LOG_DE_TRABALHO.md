# Log de trabalho

TL;DR: importação com histórico concluída na dev (merge cb81b00), README/CI/ArgoCD adaptados e materiais do 04 preservados. Main/push/PR/nuvem intactos. Integração e instrumentação locais aprovadas em 2026-10-27; conta AWS e APM externo pendentes.

Última atualização: 2026-10-27, Codex.

## 2026-10-27 11:11 (America/Sao_Paulo, UTC-03:00) — Codex — P-005/P-008 locais concluídas e handoff verificado

Feito: explicação leiga/técnica e relatório Terraform entregues; inventário reconferido sem alterar IaC: 40 .tf, sete módulos locais, oito chamadas, 51 blocos resource, 13 data e três estados S3. Baseline de 2026-10-22 preservado e regressão reexecutada em 2026-10-27. Cinco serviços instrumentados; ensaio final saída0 com 19 spans/5 serviços, PostgreSQL auth2/flag1/targeting1, Redis, HTTP e SQS produtor→consumidor→DynamoDB. Sete eventos da regressão + um controlado conferidos. Logs JSON5, sonda de sanitização e health aprovados.

Decisões/por quê: D-016 aplicada no escopo local, sem exportar New Relic conforme escolha direta do usuário. Lacuna SQL corrigida: RealDictCursor no pool/connect preserva a factory OTel; nova regressão rejeita os fontes/trace anteriores sem SQL. Verificador de padrões corrigido apenas para excluir cópias dele próprio no arquivo morto. Nenhuma credencial real foi configurada ou publicada.

Verificações: 13 testes Go principais + oito subtestes/build/vet/gofmt; 20 testes Python nas imagens reconstruídas; lint/sintaxe/QA Python e validação Collector; árvore e SQL reconferidos independentemente. 28 fontes de produção estáveis por SHA-256 durante build/teste final. 34 links locais, diff-check e padrões conhecidos aprovados; 39 materiais04 intactos, 33 exclusões anteriores mantidas, fonte03 limpa, dev/HEAD/main preservadas. Sem Terraform plan/apply, AWS, CI remoto, commit/push/PR ou memória global.

Arquivos: README.md e observability/README.md; configs Collector/Compose; scripts de ensaio/validação; fontes/testes/dependências e README dos cinco serviços. Relatórios principais em `02_TRABALHO/RELATORIO_TERRAFORM_BACKEND_2026-10-22_v01.md`, `RELATORIO_PASSO1_REVALIDACAO_2026-10-27_v01.md`, `RELATORIO_PASSO2_OBSERVABILIDADE_LOCAL_2026-10-27_v01.md`; resultado consolidado `RESULTADO_PASSOS_LOCAIS_2026-10-27_v01.json`, revisão independente e `verificacao-passos-locais-2026-10-27_v01.json`. Backups preservados nas pastas datadas de retomada/instrumentação em _ARQUIVO_MORTO; QA bruta ignorada em `02_TRABALHO/qa-passos-locais-2026-10-27/`.

Limpeza: conferidos rótulos/nomes; removidos somente 12 contêineres e dois volumes descartáveis tc04-integration em2026-10-27 11:04. Nenhum recurso desse projeto permaneceu. Imagens e traces em bind mount preservados. Evidência em cleanup-result.json.

Estado p/ o próximo agente: P-005 e P-008 concluídas; não repetir importação ou instrumentação. Para reproduzir, engine Linux+Bash+Python3 real no PATH, executar `bash scripts/test-observability.sh`; nesta sessão foi usado shim local para Python empacotado, sem mudar PATH global. E1 ainda parcial: falta conta/configuração e prova no New Relic (ingestão/trace/mapa); REQ-OBR-11 não concluído, pois métricas/coleta de logs e seus backends são próximos trabalhos E3. P-003 continua conta/backend/cotas/orçamento/identidades AWS; E2 depende dos dados e futuras autorizações de publicação/implantação. Sem reutilizar estado/segredos antigos. Prazos/grupo/submissão e cenário de falha seguem nas pendências existentes. Ler PENDENCIAS + este registro + relatórios basta para continuar sem o usuário reexplicar.

## 2026-10-27 10:57 (America/Sao_Paulo, UTC-03:00) — Codex — Integração OTel e achado de cobertura SQL

Feito: Go final instrumentado,13testesprincipais+8subtestes/build/vet aprovados; Python18testes aprovados também dentro das imagens3.12. Duas execuções integradas completas saída0:7eventosregressão+1controlado,17spans5serviçosHTTP/SQScomárvoredepaisfechada,logsJSON5,canaryprivacidadesanitizado ehealthsemspans. Fontesprodução28arquivosestáveisduranteúltimobuild/teste.

Achado: inspeçãodotrace17mostrouSQLsomenteauth,apesarPsycopg2configuradoemflag/targeting. cursor_factory=RealDictCursor porcursor substituifactoryinstrumentada. NãofecharP008ainda: agentepythonliberadoacorrigirmínimo(passarfactoryaopool/usarcursor()),preservarrowdict,addregressãoreal. GateintegradoagoraexigeCLIENTPostgreSQLnos3serviços,sobauthflagtargeting.

Arquivos/evidências: `02_TRABALHO/qa-passos-locais-2026-10-27/passo2-compose-final.log`, `otel/resultado-traces-17spans.json`, `production-sha256-final.json`; relatóriosGo/Pythonsalvos. Revisorindependenteconferiuárvore17masaprovaçãofinalsuspensa atéSQLcorrigido. Próximopasso: concluirtestepool/SQLPython,rebuild+novaprova,relatóriopasso2,limpezaapenasprojetotc04-integration,contexto/handoff. Semcommit/push/PR/AWS.

## 2026-10-27 10:43 (America/Sao_Paulo, UTC-03:00) — Codex — Retomada dos passos locais após interrupção

Feito: usuário reiterou explicação aprofundada do backend/Terraform e execução dos passos1/2. Protocolo e Git conferidos na dev, HEAD3b21e65. Preservado baseline aprovado em2026-10-22/7eventos, sem refazer/importar base. Passo2 interrompido: Python+Collector/testes criados; Go somente telemetry.go parcial sem integração/dependências. Novos agentes com escopos exclusivos Go/Python e auditoria somente leitura. NewRelic continua adiado por resposta direta anterior. Explicação fornecida antes de retomar testes.

Estado: Docker Desktop estava desligado nesta conferência; iniciado via CLI para ensaio local. Não comprova indisponibilidade permanente. Não houve operação AWS. Snapshots novos em `_ARQUIVO_MORTO/2026-10-27_retomada-passos-locais/`, estado Git em `02_TRABALHO/estado-retomada-passos-locais-2026-10-27_v01.json`, QA em `02_TRABALHO/qa-passos-locais-2026-10-27/`. Versões22 preservadas.

ChecklistP008: [x] relatórioTerraform/backend; [x] passo1aprovado22; [ ] completarGo/Python+ensaiopasso2+relatório; [ ] revisão/preservação/contexto/handoff/limpezalaboratório. Semcommit/push/PR/main/nuvem; 33exclusõespreexistentesintocadas, fonte03e39materiais04protegidos. Próximoagente: retomar passo2, conferir arquivos salvos antes de repetir; relatar resultados atuais com data27, sem redatar resultados22.

## 2026-10-22 12:04 (America/Sao_Paulo, UTC-03:00) — Codex — Terraform documentado e passo 1 aprovado

Feito: relatório Terraform/backend concluído com inventário e 64 links locais conferidos; 40 arquivos .tf, sete diretórios de módulos locais, oito chamadas e 51 blocos resource (não contagem de instâncias). Nenhuma consulta/alteração AWS. Baseline Compose aprovado antes da instrumentação: cinco serviços saudáveis, autenticação/persistência/regras/cache, atualização após TTL e sete eventos via SQS/analytics/DynamoDB simulado, saída 0.

Arquivos: `02_TRABALHO/RELATORIO_TERRAFORM_BACKEND_2026-10-22_v01.md`; `02_TRABALHO/RELATORIO_PASSO1_INTEGRACAO_LOCAL_2026-10-22_v01.md`; evidência ignorada `02_TRABALHO/qa-passos-locais-2026-10-22/passo1-compose.log`; `scripts/test-compose.sh` explicita COMPOSE_PATH_SEPARATOR para Windows/Git Bash (original preservado no snapshot inicial).

Descobertas: guard do provider AWS não protege automaticamente backend/remote_state/exec AWS CLI; conta/bucket/região reais continuam pendentes. Nenhuma instrumentação alterou o baseline. Laboratório exclusivo tc04-integration permanece temporariamente ativo para passo2; limpeza final somente dos recursos deste projeto. Não transportar estado da conta anterior.

Estado p/ o próximo agente: P-008 itens Terraform e passo1 concluídos; iniciar passo2 Go/Python + Collector local, preservar propagação HTTP e SQS e contratos de negócio, comprovar traces e regressão funcional. New Relic explicitamente adiado pelo usuário; não alegar exportação externa. Sem commit/push/PR/main/nuvem.

## 2026-10-22 11:55 (America/Sao_Paulo, UTC-03:00) — Codex — Backend/Terraform e passos locais autorizados

Feito: usuário pediu explicação/relatório aprofundado sobre backend e Terraform e autorizou executar passo1 (teste integrado) e passo2 (instrumentação local OTel), com relatório/resumo ao fim de cada passo. Explicação inicial fornecida antes da execução. Relatório IaC em elaboração por revisão independente; agentes Go/Python em preparação somente leitura, aguardando baseline aprovado. Usuário confirmou não ter New Relic: validar localmente primeiro.

Escopo: código/configuração/testes e documentação necessários no04 autorizados; manterdev. Sem commit/push/PR/main/implantaçãonuvem; Fase3 e materiaisoriginais somenteleitura. Pode criar/encerrar somente o laboratório Compose isolado destaexecução; não tocar contêineres/volumes deoutrosprojetos. Não usar AWSreal. NewRelic externo não será alegadocomovalidado.

Checklist P-008: [ ] relatórioTerraform/backend; [ ] passo1 teste+relatório; [ ] passo2 instrumentação+testes+relatório; [ ] revisão final/contexto/handoff. Originais antes dos ajustes preservados em `_ARQUIVO_MORTO/2026-10-22_passos-locais/`; manifesto dehashes/Git em `02_TRABALHO/preservacao-passos-locais-2026-10-22_v01.json`. Logs/evidências brutos locais em `02_TRABALHO/qa-passos-locais-2026-10-22/` ignorado.

Estado p/ o próximo agente: seguir a ordem autorizada; não editar/instrumentar serviços antes de registrar o baselinePasso1 aprovado. Reportar eventual falha e corrigi-la no escopo local. ChaveNewRelic ausente por confirmação do usuário; Collector/inspeção local são o destino desta execução.

## 2026-10-22 11:25 (America/Sao_Paulo, UTC-03:00) — Codex — Próximos passos e engine Docker disponível

Feito: usuário pediu próximos passos. [x] Conferidos protocolo/backlog/plano/Git; [x] verificada prontidão local; [x] revisão independente da ordem/dependências; [x] atualizados PENDENCIAS e DOSSIE. Docker respondeu servidor 29.6.1, OSType linux, Docker Desktop/contexto desktop-linux. Somente leitura: nenhum contêiner/teste foi iniciado.

Descobertas: bloqueio anterior da engine em P-005 superado; ensaio integrado continua pendente. Próxima ação é validar a base Compose (projeto tc04-integration, valores fictícios/Moto), depois E1 Go/Python + Collector/contexto HTTP/SQS. Desenvolvimento local independe da conta AWS; fechar exportação APM depende de New Relic. Conta AWS/backend/cotas/identidades e acessos PagerDuty/Slack podem ser preparados em paralelo. E2 segue base → publicação autorizada de imagens → cluster → k8s. E3–E7 preservam a ordem do plano.

Arquivos/de-para: versões anteriores de LOG/PENDENCIAS/DOSSIE preservadas em `_ARQUIVO_MORTO/2026-10-22_proximos-passos/`. Fontes: backlog, plano parte09, scripts/test-compose.sh, terraform/README.md e docker info/context show em2026-10-22. Branch dev, último commit3b21e65; alterações documentais anteriores continuam locais. Sem execução Terraform/AWS, CI remoto, commit/push/PR ou memória global.

Estado p/ o próximo agente: P-005 pronto para tentativa de ensaio, não marcado como aprovado; não repetir diagnóstico de engine indisponível como fato atual. Não iniciar implementação como se esta pergunta fosse autorização de deploy/publicação. Próximos trabalhos: ensaio base, E1 e preparação paralela de contas. Não reabrir escolhas New Relic/Slack/GitHub Actions já tomadas. Prazo informado2026-11-17, calendário a replanejar; dúvidas de grupo/submissão e cenário de falha continuam no backlog.

## 2026-10-22 11:14 (America/Sao_Paulo, UTC-03:00) — Codex — Aula 05 CI/CD: ambientes, módulos e pipelines Terraform

Feito: usuário pediu estudo da Aula 05 da Fase 3. Aplicada skill PDF em leitura; 16 páginas lidas e seis páginas com figuras/tabela renderizadas/inspecionadas. Revisões independentes conferiram ausência do exemplo de branch no PDF e uso real das três raízes/workflow do projeto. Documentação oficial HashiCorp/GitHub consultada em 2026-10-22. Checklist completo em `02_TRABALHO/aula05-terraform-2026-10-22_v01/LEITURA_E_CONFERENCIA.md`.

Descobertas: módulos reutilizam código; ambientes combinam parâmetros, recursos/identidades e estados apropriados; workspaces CLI separam estados, mas não são isolamento forte. As raízes terraform/, cluster/ e k8s/ são três camadas do prod, não três ambientes. Terraform Check da Fase 3 contém fmt/init sem backend/validate; não plan/apply/test. Branch Git não cria ambiente nem garante disparo do Actions. Plan salvo continua vinculado ao mesmo destino.

Incertezas não bloqueantes: branch específica da videoaula não localizada no PDF, que remete a prática aos vídeos; nenhuma transcrição/vídeo no repo. Tabela p. 10 tem aparente inconsistência na linha reutilização; figuras usam dev/test/prod por workspaces enquanto o texto recomenda diretórios separados. Registradas em P-007, sem atribuir exemplos complementares à FIAP.

Arquivos: extratos sem marca pessoal e leitura/conferência em `02_TRABALHO/aula05-terraform-2026-10-22_v01/`; imagens locais ignoradas em `02_TRABALHO/qa-aula05-terraform-2026-10-22/`. LOG/PENDENCIAS anteriores preservados em `_ARQUIVO_MORTO/2026-10-22_aula05-terraform/`. Fonte PDF idêntica por SHA-256 e checkout da Fase 3 limpo. Nenhuma escrita na Fase 3, execução Terraform/AWS, commit/push/PR ou alteração de arquitetura/memória global.

Estado p/ o próximo agente: explicação didática fornecida, P-007 concluída com limitação do vídeo registrada. Não reproduzir suposto código/nome de branch como conteúdo verificado da FIAP. Implementação da Fase 4 permanece em E0 parcial/P-003/P-005/E1 e refinamentos P-002, na dev. Não há mudança de código ou demanda de provisionamento decorrente desta consulta.

## 2026-10-22 10:39 (America/Sao_Paulo, UTC-03:00) — Codex — README com explicações e arquitetura revisado

Feito: P-006 concluída. README principal atualizado com síntese das explicações sobre métricas/logs/traces, OTel/Collector, Prometheus, Loki, Grafana, New Relic, PagerDuty, Slack, Actions e conceitos Kubernetes. Acrescentados papéis cluster/SaaS, contagem condicional de pods, fontes oficiais e vínculos para plano/cobertura/backlog. Três diagramas distinguem telemetria, resposta a incidentes e publicação. O plano e materiais originais não foram alterados.

Decisões/Por quê: D-015 consolida a documentação, mantendo D-009/D-012/D-014 e preservando o histórico da Fase 3. O README anterior era parcial: lista da stack e fluxo de CI/CD, sem as explicações do chat. Desenho planejado não é implantação; capacidade proposta de três workers e réplicas indefinidas do gateway mantidas como tal.

Verificação: 21 links locais aprovados; cercas Markdown íntegras; três diagramas analisados/renderizados com Mermaid major 11 via CDN no Chrome headless, capturados e inspecionados visualmente. Diagrama inicialmente amplo foi dividido em telemetria e resposta para evitar cruzamentos ambíguos. Revisão técnica independente sem achados. SHA-256 confirma 39 materiais/entregáveis preexistentes do 04 intactos; snapshot do README anterior confere; 33 exclusões locais anteriores mantidas. Dev e main conferidas, sem mudança de branch ou commit. Esta revisão não requer testes de runtime porque nenhum código/configuração operacional mudou.

Arquivos/de-para: README.md, DECISOES, DOSSIE, PENDENCIAS e este LOG atualizados; versões anteriores em `_ARQUIVO_MORTO/2026-10-22_readme-observabilidade/`. Auxiliares/evidências em `02_TRABALHO/estado-antes-readme-2026-10-22_v01.json`, `validar-readme-2026-10-22_v01.mjs`, `verificacao-readme-2026-10-22_v01.json` e `resultado-render-readme-2026-10-22_v01.json`. Capturas/preview ignorados em `02_TRABALHO/qa-readme-2026-10-22/`; CDN usada apenas para QA, sem dependência nova nos entregáveis.

Estado p/ o próximo agente: P-006 encerrada; README reúne os conceitos principais e arquitetura escolhida. Continuar na dev com P-003/P-005/E1 e refinamentos de P-002. LOG + PENDENCIAS deixam claro o que foi feito e o que falta; nenhuma decisão de réplicas, teste integrado ou implantação foi antecipada. Alterações documentais permanecem locais, sem commit/push/PR/nuvem ou memória global. Não alterar as exclusões preexistentes nem repetir a importação.

## 2026-10-22 10:30 (America/Sao_Paulo, UTC-03:00) — Codex — Conferência e complementação do README

Feito: usuário perguntou se as explicações e arquitetura estão documentadas no README. Leitura confirmou tecnologias/estado de importação presentes, mas faltam sinais, papéis detalhados, SaaS versus cluster, objetos Kubernetes e diagrama de observabilidade. Revisão independente confirmou lacunas e limites do plano. Iniciada complementação documental na dev, sem alterar decisões de arquitetura.

Checklist P-006: [x] comparar README/plano/decisões; [ ] completar texto e diagramas; [ ] verificar links, Mermaid e fidelidade; [ ] atualizar contexto e handoff.

Arquivos/de-para: snapshot integral dos cinco documentos que poderão ser atualizados em `_ARQUIVO_MORTO/2026-10-22_readme-observabilidade/`, preservando caminhos relativos; manifesto em `02_TRABALHO/estado-antes-readme-2026-10-22_v01.json`. Alterações/exclusões anteriores de arquivos foram inventariadas e serão preservadas. Sem commit, push, PR ou nuvem.

Estado p/ o próximo agente: P-006 em andamento; README deve distinguir desenho planejado de implementação ainda pendente. Três workers são proposta; gateway sem réplicas fixadas. Retomar pela primeira etapa pendente de P-006, sem repetir a importação.

## 2026-10-21 10:32 (America/Sao_Paulo, UTC-03:00) — Codex — Pods, nós e padrões do Collector

Feito: esclarecimento didático solicitado sobre Pod/contêiner, nó, agent, DaemonSet, gateway e Deployment. [x] Conceitos conferidos nas fontes oficiais; [x] plano revisado quanto à contagem; [x] revisão independente confirmou os limites da inferência.

Fontes consultadas em 2026-10-21: https://kubernetes.io/docs/concepts/workloads/pods/ ; https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/ ; https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ ; https://opentelemetry.io/docs/collector/deploy/agent/ ; https://opentelemetry.io/docs/collector/deploy/gateway/ . Plano: partes 04-plataforma, 06-telemetria e 09-plano-fontes.

Descobertas: um Pod contém um ou mais contêineres; agent/gateway são papéis do Collector, e DaemonSet/Deployment são recursos de gerenciamento de pods. O plano prevê três workers e um agent por nó elegível, mas não fixa réplicas do gateway. Fórmula em situação estável: nós elegíveis + réplicas do gateway. Exemplo condicional com três workers: três agents e um gateway totalizam quatro pods do Collector; com dois gateways, cinco. Não é decisão de capacidade nem quantidade implantada. O gateway pode compartilhar worker com outros pods; não foi previsto nó dedicado.

Arquivos/de-para: apenas LOG atualizado; versão anterior preservada em `_ARQUIVO_MORTO/2026-10-21_explicacao-pods-collector/LOG_DE_TRABALHO.md`. Sem alterações de código, plano, pendências ou decisões; sem commit/push/PR/nuvem ou memória global.

Estado p/ o próximo agente: explicação conceitual fornecida. E0 parcial, P-003/P-005 e refinamentos de P-002 continuam como registrados; E1/E3 ainda pendentes. Não converter o exemplo de uma réplica do gateway em decisão já aprovada/configurada.

## 2026-10-21 09:50 (America/Sao_Paulo, UTC-03:00) — Codex — Explicação dos sinais e ferramentas de observabilidade

Feito: usuário pediu explicação didática sobre OTel Collector, New Relic, Grafana, Loki, PagerDuty e métricas/logs/traces, com casos de uso e complementaridade. Conferidos o plano de telemetria/resposta e documentação oficial em 2026-10-21. Exemplos de falha e valores usados na explicação são ilustrativos, sem alegação de execução ou exigência adicional da FIAP.

Verificação: [x] conceitos conferidos em fontes primárias; [x] separadas capacidades gerais dos produtos e funções escolhidas no projeto; [x] revisão independente da topologia e do código. Métricas mostram medições/tendências; logs registram eventos; traces relacionam operações de uma execução. OTel instrumenta/coleta/transporta; Collector recebe/processa/exporta; Prometheus armazena métricas, Loki logs, Grafana consulta/visualiza e avalia alertas; New Relic é o APM previsto; PagerDuty gerencia incidentes e responsáveis. GitHub Actions executará a tentativa de mitigação prevista, em fluxo separado do acionamento humano.

Fontes: https://opentelemetry.io/docs/collector/ ; https://opentelemetry.io/docs/concepts/observability-primer/ ; https://docs.newrelic.com/docs/opentelemetry/opentelemetry-introduction/ ; https://docs.newrelic.com/docs/opentelemetry/get-started/apm-monitoring/opentelemetry-apm-intro/ ; https://grafana.com/docs/grafana/latest/datasources/ ; https://grafana.com/docs/loki/latest/get-started/overview/ ; https://docs.pagerduty.com/incident-management/incidents/overview ; https://prometheus.io/docs/introduction/overview/ . Plano local: partes 06-telemetria/07-resposta e D-009.

Arquivos/de-para: somente este LOG atualizado; versão anterior preservada em `_ARQUIVO_MORTO/2026-10-21_explicacao-observabilidade/LOG_DE_TRABALHO.md`. Sem alteração de código/plano, commit, push, PR, operação de nuvem ou memória global. Pendências e decisões permanecem as já registradas.

Estado p/ o próximo agente: explicação conceitual fornecida; E1 ainda não implementada. Continuar na dev, com E0 parcial/P-003/P-005 e refinamentos de P-002. Não apresentar os fluxos de telemetria como já operacionais. O cache muda o caminho executado, e a propagação do contexto até a SQS/analytics ainda depende da instrumentação futura.

## 2026-10-21 09:36 (America/Sao_Paulo, UTC-03:00) — Codex — Conferência da cobertura do plano

Feito: usuário perguntou se temos plano com todos os obrigatórios. Conferidos README de requisitos, plano v02, situação atual e decisões pertinentes, com revisão independente. Os 42 IDs estão alocados nas etapas E0–E7, mas isso não comprova implementação nem significa que os critérios de aceite estejam completos.

Descobertas: detalhar teste funcional da base no cluster (01–05), conta APM e omissão do 12 na frase-síntese, acionamento do responsável pelo PagerDuty (17); confirmar entrega individual/grupo (41) e horário/canal oficial de submissão (42). Calendário de 2026-09-23 precisa refletir a execução atual. Dúvidas técnicas do cenário de falha e alvo do reinício permanecem abertas. Nenhuma decisão nova substitui D-009/D-014.

Arquivos/de-para: criado `02_TRABALHO/CONFERENCIA_PLANO_FASE4_2026-10-21_v01.md`; P-002 atualizado com os refinamentos. Versões anteriores de LOG/PENDENCIAS preservadas em `_ARQUIVO_MORTO/2026-10-21_conferencia-plano`. Plano, código e materiais não alterados. Exclusões locais preexistentes de 33 materiais históricos da Fase 3 foram apenas observadas e mantidas; não foram feitas por esta sessão. Sem commit/push/PR/nuvem ou atualização de memória global.

Verificação: união dos IDs por etapa igual ao conjunto dos 42 REQ-OBR do README; revisão independente separou cobertura de escopo de critérios de aceite. Links do registro de conferência verificados.

Estado p/ o próximo agente: continuar na dev. Importação P-004 concluída; E0 parcial, P-003/P-005 pendentes. O plano existe e cobre o escopo, mas precisa dos refinamentos de P-002 antes de ser tratado como plano fechado. Não repetir importação, não alterar main, não tocar nas exclusões locais do usuário.

## 2026-10-20 18:30 (America/Sao_Paulo, UTC-03:00) — Codex — Handoff e memória conferidos

Feito: memória global atualizada por pedido explícito do usuário em `C:/Users/Gabriel/.codex/memories/extensions/ad_hoc/notes/2026-10-20T18-29-00-tech-challenge-04-importacao.md`, sem credenciais ou dados da conta. LOG, PENDENCIAS, DECISOES e DOSSIE registram a importação concluída e os limites da validação. Revisão independente de continuidade apontou uma ambiguidade no snapshot anterior à autorização; a seção 14 do DOSSIE agora está rotulada como histórica e superada pela seção 15.

Decisões/Por quê: D-014 mantém a dev como ramo de trabalho; `import-fase3` preservada e já integrada. Não houve push, PR, mudança na main ou operação AWS. Nenhum trabalho de observabilidade foi declarado como implementado.

Verificação final: os 39 arquivos preexistentes de docs/enunciado da Fase 4 continuam idênticos por SHA-256; os 933 arquivos do manifesto inicial continuam presentes. As duas bases e `import-fase3` são ancestrais da dev. Main do 04 continua em `003a707`, Fase 3 continua limpa em `6100879`. Validações de código/configuração descritas no relatório permanecem aprovadas; integração Docker não executada por indisponibilidade da engine. O teste de handoff foi satisfeito: LOG + PENDENCIAS identificam o estado atual e os próximos passos sem repetir a importação.

Arquivos/de-para: atualizados `LEIA-PRIMEIRO.md`, `PENDENCIAS_E_PROXIMOS_PASSOS.md`, `LOG_DE_TRABALHO.md`, `DECISOES.md`, `DOSSIE_CONTEXTO.md` e `02_TRABALHO/RESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md`. Versões anteriores do contexto preservadas em `_ARQUIVO_MORTO/2026-10-20_fechamento-importacao`. Evidência Git em `02_TRABALHO/integracao-dev-2026-10-20_v01.json`.

Estado p/ o próximo agente: P-004 concluída; continuar na dev. P-003 aguarda a conta e configuração de backend/cotas/orçamento; P-005 aguarda Docker para executar `bash scripts/test-compose.sh`; E1 vem depois. Não usar estado ou identidades da conta antiga; não repetir importação nem publicar sem pedido. O próximo commit local somente documenta este fechamento, sem alterar código.

## 2026-10-20 18:20 (America/Sao_Paulo, UTC-03:00) — Codex — Importação concluída e merge na dev

Feito: importação com histórico da base6100879 viaimport-fase3, preservando materiais04. Checkpoint4c76a2d, mergehistórico491cd2b, adaptação31f92e4 e merge localcb81b00 na dev. Main04 segue003a707; branchimport preservada; source03 limpo. README/CI/CD/Argo/OIDC repo04, estados próprios, guards da conta e sentinelas pendingAWS preparados.

Decisões/Por quê: D-014 executa autorização desta sessão. DadosAWS ainda pendentes; nenhum recurso, CIremoto, push ou PR. Prodsegue main como destino futuro; trabalho atualna dev. Guias/insumos preservados; acervo03 separado pelo inventário.

Verificação: todos933arquivos preexistentes mantidos;39docs/enunciado04 intactos porhash. BuildsGo e ASTPython aprovados; Go não tem testesunitários. Terraform3initsembackend/3validate/fmt, 23objetosGitOps,9YAML e10casosguardAWS, Bash, Composeconfig e5guias/README/links aprovados. Revisão independente achou P2 no globdosguias, corrigido e revalidado. Composeintegrado NÃO executado: DockerLinuxengine indisponível, start50stimeout; P-005. actionlint ausente, usado parserYAML/regraslocais. Arquivosarquivados preservam aformatação original; diff--check do código vigente aprovado (snapshot.gitignore herdado temblanklineEOF).

Arquivos/de-para: relatórioRESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md, manifesto/verificação/integracaoJSON, README,CLAUDE,.github,Terraform,GitOps e3ferramentasdeguias. Originais substituídos em_ARQUIVO_MORTO/FASE3_BASE_6100879 e2026-10-20_ferramentas-guias. Contexto/LOG/PENDENCIAS/DECISOES antes deste fechamento movidos para2026-10-20_fechamento-importacao; histórico do LOG atual mantido. Renderizações/extrações~230MB preservadas localmenteignoradas.

Memória: usuário pediu atualização explícita; nota durável será gravada em C:/Users/Gabriel/.codex/memories/extensions/ad_hoc/notes com branch/escopo/pendências, sem credenciais ou dados da conta.

Estado p/ o próximo agente: trabalhar somente na dev; importaçãoP-004 concluída. Aguardar conta paraP-003/E0restante; iniciarDocker/repetirensaioP-005 e partirE1. Não repetirimportação, não alterar03/main, não publicarsem pedido. Contexto vigente00_COLAB_IA na raiz; docs/00_COLAB_IA é histórico03.

## 2026-10-20 16:20 (America/Sao_Paulo, UTC-03:00) — Codex — Início da importação autorizada

Feito: autorização explícita recebida para importação, branch import-fase3, commits/merge local na dev e ajustes README/CI/CD/ArgoCD. Conferido source 61008794090f582c098e2edc42041339c556f14c, limpo; 04 dev=9696185/main=003a707. Manifesto SHA-256 de todos os arquivos atuais salvo antes da importação, inclusive auxiliares locais.

Decisões/Por quê: D-013 passou de proposta para método autorizado nesta sessão. Só commits necessários locais; não publicar nem abrir PR; não tocar main ou Fase3. Dados AWS pendentes: preservar infraestrutura como código e remover dependência operacional de conta antiga, sem deploy.

Arquivos/de-para: snapshot inicial de LEIA-PRIMEIRO/LOG/PENDENCIAS em _ARQUIVO_MORTO/2026-10-20_inicio-importacao; manifesto 02_TRABALHO/preservacao-importacao-2026-10-20_v01.json. Mantidos todos os arquivos existentes.

Estado p/ o próximo agente: preparar checkpoint curado e importar histórico em import-fase3; depois ajustar CI/Argo/README, validar, integrar na dev e atualizar contexto/memória. Checklist incremental em P-004.

## 2026-10-20 15:43 (America/Sao_Paulo, UTC-03:00) — Codex — AWS mantida e recomendação de importação Git

Feito: usuário decidiu continuar AWS e disse que pretende criar outra conta. Conferência somente leitura: Fase3 main/dev=6100879, checkout limpo; Fase4 dev=9696185/main=003a707, materiais de trabalho não rastreados. Comparação independente das árvores: sem colisões de caminhos exatos. Elaborado plano de importação preservando os dois históricos.

Decisões/Por quê: D-012 registra escolha AWS, sem presumir novo crédito ou conta criada. D-013 recomenda merge dos históricos numa branch do 04, preservando o 03. O método ainda não foi aprovado/executado; pergunta atual do usuário era sobre a melhor opção. Não houve commit/push, fetch, branch nova ou mudança de remote.

Arquivos/de-para: criado 02_TRABALHO/PLANO_IMPORTACAO_FASE3_2026-10-20_v01.md. Versões anteriores de LOG, PENDENCIAS, DOSSIE e DECISOES movidas para _ARQUIVO_MORTO/2026-10-20_importacao-proposta/ antes das atualizações; entradas antigas do LOG preservadas integralmente.

Descobertas: F-016 — FAQ/termos oficiais AWS consultados em 2026-10-20 excluem cliente que já tem/teve conta do novo Free plan/crédito e benefícios adicionais por criar mais contas. Fontes: https://aws.amazon.com/free/free-tier-faqs/ e https://aws.amazon.com/free/terms/. Plano de custos não pode assumir crédito renovado. Estado e identidades da conta anterior não devem ser usados como se fossem recursos de outra conta.

Estado p/ o próximo agente: provedor AWS definido; E0 continua pendente. Antes da importação, preparar checkpoint revisável dos materiais do 04 e obter autorização para commits quando necessária. Fonte recomendada 6100879; método documentado em D-013. Configuração da conta/backend/OIDC/ECR e validação local vêm antes de publicar/deploy. Sem alterar a Fase3.

## 2026-10-13 16:27 (America/Sao_Paulo, UTC-03:00) — Codex — Estado do projeto e avaliação Azure

Feito: leitura de protocolo, pendências, histórico, dossiê, decisões, requisitos, verificações e plano v02. Auditoria somente leitura do código da Fase 3. Validador dos cinco guias e README: 0 erros; hashes de 32 PDFs/689 páginas: intactos. Confirmado: repositório 04 não contém services/terraform/gitops/workflows; implementação parou antes de E0, apesar de requisitos, guias e plano prontos.

Decisões/Por quê: D-009 continua como base; Azure é hipótese, não decisão aprovada. Recomendação: E0/E1 local primeiro; comparar sessões curtas AWS com Azure elegível. Q-01 permanece relevante (PDF p.2 admite AKS; roteiro p.5 nomeia EKS). Nenhuma operação de nuvem, commit/push ou migração executada.

Arquivos/de-para: criado 02_TRABALHO/ANALISE_ESTADO_E_OPCOES_CLOUD_2026-10-13_v01.md. LOG, PENDENCIAS, DOSSIE e DECISOES anteriores movidos integralmente para _ARQUIVO_MORTO/2026-10-13_auditoria/ antes das atualizações; LOG mantém todas as entradas antigas no arquivo atual.

Descobertas: F-013 — usuário informou em 2026-10-13 que crédito AWS acabou; Billing/tipo da conta/recursos ativos não verificados. F-014 — ofertas Azure oficiais: US$200/30 dias para novo cliente; Students US$100/12 meses sujeito à elegibilidade; AKS Free cobra recursos dos nós e há limites de cotas. Fontes e consulta 2026-10-13 no relatório. F-015 — instruções antigas de retomar V eram obsoletas; V já concluída, retomada efetiva é E0. Revisão visual final dos guias continua com limitação registrada, não confundida com o teste estrutural.

Estado p/ o próximo agente: P-003 aguarda escolha de provedor/benefício/cotas/orçamento e esclarecimento Q-01. P-002 em E0; planejamento antigo AWS precisa ser revisto após decisão. Prazo do usuário 2026-11-17 (35 dias desde 2026-10-13), não data do PDF. Começar por trabalho local reaproveitável. Sem perguntas refeitas sobre New Relic/Slack/GitHub Actions já definidos.

## 2026-09-24 01:42 (America/Sao_Paulo, UTC-03:00) — Claude (Opus 5.5) — Plano de ação e arquitetura da implementação (v02)

Contexto: o usuário pediu o plano para subir o projeto atendendo todos os requisitos, com diagramas de alto e baixo nível "desde o push na dev até a exibição das métricas", sem inventar dados e perguntando nas dúvidas. O plano v01 (Markdown, 2026-09-21) foi refeito do zero.

Feito:
- Leitura do código real da Fase 3 (`tech-challenge-03`, somente leitura): os 7 workflows, as três camadas do Terraform, `argocd.tf`, módulo `iam-ci`, `gitops/`, os cinco serviços (Dockerfile, dependências, `main.go`, `evaluator.go`, `sqs.go`, `app.py`), os dois Compose e a estimativa de custo arquivada.
- Decisões tomadas pelo usuário por pergunta direta: código migra para o 04 (Fase 3 congelada), New Relic, Slack, self-healing por GitHub Actions, implementação solo, entrega em 2026-11-17 (a data veio do usuário, não do PDF). Ambiente AWS: desconhecido.
- 17 fatos externos conferidos na documentação oficial (Loki OTLP, spanmetrics, ArgoCD diffing, repository dispatch, webhook do Grafana, fork no Python, access policies do EKS, values do kube-prometheus-stack 91.5.0 e do chart do Collector 0.173.1, otelsql, redisotel v8, instrumentações AWS para Go, psycopg2-binary, telas do New Relic para OTel).
- Documento HTML autocontido montado de 9 partes em `02_TRABALHO/plano-fase4/partes/`: 1 diagrama de alto nível, 5 de baixo nível (commit ao pod, Terraform x ArgoCD, requisição e trace, pipelines do Collector, alerta à correção), inventário de arquivos, plano E0–E7, calendário, custo, riscos, perguntas e fontes.
- Validação: estrutura HTML, IDs, 22 âncoras internas e os 6 SVG como XML — 0 erros. Revisão visual por Chrome headless (claro e escuro), 3 defeitos de rótulo corrigidos e re-renderizados. Uma frase que atribuía à aula de Alert Fatigue práticas que ela não lista foi reescrita com o que o guia de Incidentes registra (Aula 2, p. 6 e 14–16; Aula 4, p. 7–9).
- Plano v01 movido para `_ARQUIVO_MORTO`.

Achados que o plano incorpora: o `evaluation` usa `context.Background()` global (spans órfãos sem mudar as assinaturas); a SQS precisa de propagação manual (contrib só instrumenta `aws-sdk-go-v2`); erro no `targeting` não vira 5xx no `evaluation`; cache de 30 s; HPA com `replicas: 1` no Git e `selfHeal` sem `ignoreDifferences`; webhook do Grafana também envia `resolved`; crédito AWS limitado (~190 h em 2026-09-09) e EKS 1.34 em suporte padrão até 2026-12-01.

Estado p/ o próximo agente: plano entregue; sete perguntas em aberto no documento (seção "Perguntas em aberto"). Para alterar, edite a parte em `plano-fase4/partes/` e remonte com `cat plano-fase4/partes/0*.html > PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html`. Nada foi implantado. Sem commit/push.

## 2026-09-21 08:05 (America/Sao_Paulo, UTC-03:00) — Claude (Opus 5) — Verificação final concluída

Contexto: a terceira execução com subagentes (4 verificadores) também caiu por limite de sessão, sem gravar arquivos. A verificação foi refeita no laço principal, conforme D-007.

Feito:
- Checagem automatizada de cobertura total: `conferir-codigo-2026-09-21_v01.py` comparou os tokens dos 72 blocos de código dos fragmentos de APM e Incidentes com a extração da aula correspondente — 63 confirmados direto no texto; os 9 restantes são transcrições de figuras (Serilog, middleware, cabeçalhos, máscara), conferidas nas páginas renderizadas na hora da escrita. Nenhum bloco escrito por subagente ficou abaixo do limiar.
- Conferência de 253 referências `#page=N` contra a página citada no texto do link: 3 incoerentes, todas no fragmento `08-aula-07.html` (link abria a última página do intervalo). Corrigidas no fragmento, guia remontado e revalidado.
- Amostragem dirigida de 12 afirmações do material escrito por subagentes, conferidas na extração: todas corretas. Três achados `[INCERTO]` deles foram validados de forma independente (APM-A07-Q02, APM-A07-Q03, APM-I03, APM-A09-Q01).
- Registro completo em `02_TRABALHO/verificacoes/verificacao-final-2026-09-21_v01.md`.

Resultado final: `validar-guias-2026-09-16_v01.py` sem erros nos cinco guias e no README; 32 PDFs originais intactos por SHA-256; nenhum dado pessoal do titular nos entregáveis.

Estado p/ o próximo agente: nada pendente em P-001. Se quiser fechar a revisão visual, abra os cinco guias no navegador em tela ampla e estreita — o acesso a `file://` estava bloqueado no painel desta sessão. Para alterar qualquer guia, edite o fragmento ou o script gerador e remonte; nunca edite o HTML final. Sem commit/push.

## 2026-09-21 04:20 (America/Sao_Paulo, UTC-03:00) — Claude (Opus 5) — B4 concluído, fechamento C e verificação final

Contexto: a tentativa de escrever o B4 com 12 subagentes (2026-09-20 22:00) caiu no limite de sessão. Três agentes, porém, gravaram seus fragmentos antes de morrer — aulas 7, 8 e 9 —, e eles foram conferidos, validados e aproveitados. As demais sete aulas foram escritas por mim, inline, uma a uma, gravando cada fragmento assim que ficava pronto.

Feito:
- **B4 (APM) concluído**: 18 fragmentos em `fragmentos/apm/`, montados em `GUIA-ESTUDO-APM.html` — 391 KB, 19 seções, 66 blocos de código, 19 complementos, 27 IDs de requisito na seção de conexão. Leitura integral das 335 páginas; todas as páginas com código, tabela ou figura informativa foram conferidas nas imagens renderizadas antes de transcrever.
- Ferramentas novas: `preparar-leitura-2026-09-21_v01.py` (limpa cabeçalhos repetidos da extração e mapeia páginas com código/figura) e `mapear-modulos-readme-2026-09-20_v01.py` (preenche a coluna "Módulo(s)" a partir da cobertura real dos guias).
- **Fechamento C**: coluna "Módulo(s)" preenchida nas 44 linhas do README a partir de quem cita cada requisito na seção de conexão — nada inventado; REQ-OBR-21 passou a ser citado pelo guia de APM e REQ-OBR-25 ficou como "Fases 1–3 (base anterior)". Índice da §11 publicado com os cinco guias. Espelho `REQUISITOS.html` regenerado.
- **Integridade**: os 32 PDFs originais conferidos por SHA-256 contra o inventário — 32 intactos, 0 alterados.
- **Validação**: `validar-guias-2026-09-16_v01.py` passa nos cinco guias e no README com 0 erros. Auditoria estrutural de responsividade: 113 tabelas, todas dentro de `.tablewrap`; nenhuma largura fixa; `viewport` e 9 media queries em cada arquivo.
- F-004 conferido e **já resolvido** pela sessão de 17/09: o Código Fonte 1 da Aula 4 de Observabilidade está transcrito integralmente no guia, batendo com a imagem da p. 10.
- Verificação adversarial final lançada com 4 agentes (Datadog, New Relic, Incidentes e seções transversais), gravando achados em `02_TRABALHO/verificacoes/`.

Descobertas registradas nos guias: as incertezas APM-I01 a APM-I05 (Codex) foram confirmadas e documentadas, e outras 14 foram acrescentadas (APM-A01-Q01 a APM-A09-Q03). Destaque: o próprio módulo se contradiz nas Core Web Vitals — a Aula 5 lista FID e a Aula 10 lista INP (APM-I04).

Limitação: `file://` deixou de ser acessível no painel do navegador durante esta sessão (funcionou em 2026-09-16 no guia de Opensource, sem rolagem horizontal a 1280 px). A revisão visual final dos guias novos não pôde ser repetida no navegador; foi substituída por auditoria estrutural.

Estado p/ o próximo agente: aplicar os achados de `02_TRABALHO/verificacoes/` (se houver), reexecutar `validar-guias` e, se possível, abrir os cinco guias no navegador em tela ampla e estreita. Sem commit/push.

## 2026-09-20 21:50 (America/Sao_Paulo, UTC-03:00) — Claude (Opus 5) — Conserto de links, B5 montado, README corrigido, B4 em autoria

Contexto: a execução de 2026-09-16 22:20 (32 subagentes: leitura das 31 aulas + auditoria do README) foi interrompida pelo limite semanal de uso da conta. Dois artefatos foram gravados antes da interrupção e estão aproveitados: `dossies/dossie-welcome-capitulo-2026-09-16_v01.md` e `auditorias/auditoria-readme-requisitos-2026-09-16_v01.md`. Os demais 30 agentes morreram sem gravar.

Feito:
- F-009: os três guias regenerados em 2026-09-17 apontavam para `../../requisitos/REQUISITOS.html`, que não existia (D-006 decidida, espelho não criado). Eram 13 a 40 links quebrados por guia. Corrigido criando o espelho com `gerar-espelho-requisitos-2026-09-20_v01.py`, que converte o README (fonte de verdade) em HTML com as 48 âncoras, mesmo CSS e aviso de arquivo gerado.
- F-010: `criar-fragmentos-incidentes-2026-09-17_v01.py` estava completo (16 fragmentos + conexões + configuração), mas nunca havia sido executado. Executado e montado: **B5 pronto** — `GUIA-ESTUDO-Automacao-de-incidentes.html`, 90 KB, 17 seções, 6 blocos de código, 16 complementos, validação sem erros.
- Auditoria do README aplicada por `aplicar-auditoria-readme-2026-09-20_v01.py` (achados 1 e 3–18, cada substituição conferida por contagem): novo REQ-OBR-42 (submeter no prazo), textos de REQ-OBR-05, 08, 10, 11, 17, 26, 27, 30 e dos dois REQ-BON ajustados ao enunciado, critérios (a)(b)(c) no checklist, §2/§3/§4/§5/§8 corrigidas e dúvidas Q-08 a Q-14 acrescentadas. README passa a ter 42 obrigatórios, 2 bônus, 4 sugestões e 14 dúvidas; versão anterior em `_ARQUIVO_MORTO/README-requisitos-2026-09-16_v01-codex.md`.
- B4 (APM) lançado com 12 subagentes: um autor por aula (leitura integral, conferência visual do código e fragmento HTML validado) e dois para as seções transversais.

Decisões/Por quê: manter e estender o trabalho do Codex de 17/09 (fragmentos do módulo Incidentes seguem a especificação e têm boa qualidade) em vez de refazer; aplicar a auditoria do README agora, porque ela já estava paga e traz o requisito de submissão que faltava; espelho HTML gerado por script para não criar segunda fonte de verdade.

Estado p/ o próximo agente: falta (1) terminar B4 e montá-lo; (2) verificação adversarial de fidelidade dos guias B1–B5 contra as fontes, com correção do que for confirmado — inclusive F-004 (Código Fonte 1 da Aula 4 de Observabilidade ainda transcrito pela metade); (3) fechamento C — preencher a coluna "Módulo(s)" e o índice §11 do README, revisão visual no navegador, conferência de hashes dos originais e handoff. Sem commit/push.

## 2026-09-17 11:41 (America/Sao_Paulo, UTC-03:00) — Codex — Retomada após Claude

Feito: protocolo, pendências, log, decisões e dossiê lidos. Três HTMLs existem; validação estática inicial de Claude retornou zero erros. Auditoria README e dossiê Welcome aproveitados. B4/B5 retomados por subagentes com contexto preservado; B3 em auditoria independente.

Decisões/Por quê: D-006 cria espelho HTML dos requisitos para resolver navegação local (F-007). D-005 aplicado à revisão de B1/B2, mantendo scripts v01 e criando v02. Extração PDFium recuperou texto integral: a hipótese anterior de rasterização generalizada era incorreta; falhava o modo layout do pypdf.

Arquivos/de-para: guia_base.py anterior movido para _ARQUIVO_MORTO/2026-09-17_revisao/guia_base-2026-09-16_v02-claude.py; guias B1/B2 movidos para a mesma pasta com sufixo -2026-09-16_v01.html antes da nova geração. Novo gerador criar-guias-fundamentos-2026-09-17_v02.py.

Descobertas: F-008 atualizado com fonte oficial de preços da Atlassian: novos cadastros OpsGenie encerrados em 2025-06-04; encerramento do acesso em 2027-04-05. Fonte: https://www.atlassian.com/software/opsgenie/pricing, consulta 2026-09-17. Não altera a regra FIAP automaticamente.

Estado p/ o próximo agente: gerar/revisar B1/B2 v02; concluir B3–B5; revisar README com achados de Claude, espelho e links; validação estática/visual e hashes; depois marcar C. Sem commit/push.

## 2026-09-16 22:04 (America/Sao_Paulo, UTC-03:00) — Claude (Opus 5) — Retomada e auditoria do estado deixado pelo Codex

Feito: leitura de LEIA-PRIMEIRO, PENDENCIAS, LOG, DECISOES, DOSSIE, ORGANIZACAO; inventário de `02_TRABALHO`; leitura integral do README de requisitos contra o texto do enunciado (p. 1–7); leitura do modelo CI/CD da Fase 3; leitura de `guia_base.py`, CSS base e dos dois guias HTML existentes.

Descobertas (trabalho do Codex posterior a 15:27, sem entrada no LOG):
- F-003: 21:23–21:29 — `criar-guias-fundamentos-2026-09-16_v01.py` gerou os guias B1 (Welcome) e B2 (Observabilidade); `cobertura-fundamentos-2026-09-16_v01.md` declara leitura integral de 87 páginas. Checklist não foi marcado nem os guias validados.
- F-004: B2 transcreve apenas 4 linhas do Código Fonte 1 (Aula 4, p. 10) e incorpora o restante como imagem PNG base64; o texto completo do YAML é extraível por PDFium. Pendente de correção (exigência de código preservado).
- F-005: B3 (Opensource) — leitura integral declarada (118 p.), `criar-guia-opensource-2026-09-16_v01.py` compila e está completo, mas o HTML nunca foi gerado nem validado.
- F-006: B4 (APM, 10 PDFs, 335 p.) — `cobertura-apm-2026-09-16_v01.md` registra leitura das aulas 1–5 e incertezas APM-I01–I05; aulas 6–10, autoria e validação pendentes. B5 (Incidentes, 7 PDFs, 142 p.) — apenas extrações e renderizações em `qa-incidentes/`; sem nota de cobertura nem guia.
- F-007: links dos guias para `README.md#req-obr-NN` funcionam no GitHub; abertos localmente por duplo clique, o navegador mostra o Markdown como texto e não rola até a âncora. Limitação a registrar no fechamento.
- README (Fase A) conferido: evidências batem com o texto das p. 2–6; nenhuma correção bloqueante encontrada.

Decisões/Por quê: continuar sobre a infraestrutura do Codex (CSS base e `guia_base.py`) para manter consistência visual; auditar B1–B3 contra as fontes antes de marcá-los; produzir B4/B5 com leitura por aula, inspeção visual de páginas com código/figuras e verificação adversarial.

Estado p/ o próximo agente: ver PENDENCIAS (P-001 com subetapas atualizadas). Python com pypdfium2: `C:\Users\Gabriel\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` (o `python` do PATH não tem pypdfium2). Sem commit/push.

## 2026-09-16 15:27 (America/Sao_Paulo, UTC-03:00) — Codex — B0 concluída

Feito: modelo CI/CD lido integralmente; esqueleto didático/visual registrado; CSS comum e gerador criados.

Decisões/Por quê: preservar base visual e explicação simples → técnica; acrescentar sumário, evidência por página e Complemento. Sem dependências externas.

Arquivos: 02_TRABALHO/analise-modelo-guia-2026-09-16_v01.md, guia_base.py e guia-base-2026-09-16_v01.css.

Estado p/ o próximo agente: B1–B5 serão produzidos a partir do registro de requisitos já fixado. Checklists e LOG centrais são editados apenas pelo agente principal.

## 2026-09-16 15:25 (America/Sao_Paulo, UTC-03:00) — Codex — Fase A concluída

Feito: README salvo com 41 REQ-OBR, 2 REQ-BON (opções/preferências sem pontos extras), 4 SUG e 7 dúvidas Q-01–Q-07. Leitura integral de 7 páginas; auditoria independente e inspeção visual das imagens das p. 1 e 7 confirmaram ausência de anexos/requisitos adicionais.

Decisões/Por quê: D-002; status Pendente em todos os requisitos. Requisitos conservadores para vídeo EKS/ArgoCD e grupo, com incertezas explícitas. Prazo da Fase 3 não transferido.

Arquivos: docs/requisitos/README.md; 02_TRABALHO/registro-requisitos-2026-09-16_v01.json; gerador; PENDENCIAS.

Descobertas: F-002 e sete questões ao tutor documentadas no README.

Estado p/ o próximo agente: iniciar B0 (modelo completo); em seguida B1–B5, conferindo todos os PDFs e imagens relevantes. A concluída antes da B.

## 2026-09-16 15:23 (America/Sao_Paulo, UTC-03:00) — Codex — Preparação

Feito: localização e permissões conferidas; cinco pastas encontradas; 32 PDFs extraídos integralmente (31 aulas + enunciado). Inventário com páginas e hashes salvo. Leitura do enunciado p. 1–7 e estrutura do checklist histórico da Fase 3 iniciadas. Auditoria independente do enunciado delegada a subagente.

Decisões/Por quê: D-001 concentra auxiliares em pasta autorizada; D-002 separa exigência documental de implementação. Não foi criado CLAUDE.md na raiz, pois a regra específica de caminhos não autoriza escrita ali.

Arquivos: seis documentos de `00_COLAB_IA`; `02_TRABALHO/extrair-fontes-2026-09-16_v01.py`, inventário e extrações.

Descobertas: F-001, F-002. A impressão final do script encontrou limitação cp1252 em nome com acento decomposto; arquivos UTF-8 foram todos salvos antes do erro. Próximas execuções usarão Python `-X utf8`.

Estado p/ o próximo agente: P-001, etapa A. Inspecionar páginas com imagens/baixa extração; terminar e salvar README antes de iniciar autoria da Fase B. Sem commit/push.


