# Pendências e progresso

TL;DR: P-016 concluída em 2026-11-01: memória da Fase 3 consolidada e 39 originais arquivados. D-018 aprovada; aplicação pública no B6/P-017. Retomar B0/B1; P-013/P-014 ainda precisam de fechamento documental.

Última atualização: 2026-11-01, Codex (continuação do Claude).

## P-016 — Mesclar a colaboração da Fase 3 e retirar a pasta redundante (concluída, 2026-11-01)

Pedido autorizado do usuário em 2026-11-01, iniciado pelo Claude e concluído pelo Codex após a interrupção. Relatório: [MESCLA_COLAB_FASE3_2026-11-01_v01.md](02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md).

- [x] Reaproveitar extração dos 39 arquivos, rascunhos e backups, sem repetir a importação de código.
- [x] Revisar e incorporar 59 decisões F3-D/F3-SN, dossiê §20, pendências herdadas e regras de colaboração/organização. Índice rastreia 158 conhecimentos e 39 registros de pendência (inclui duplicatas/históricos).
- [x] Atualizar ponteiros CLAUDE.md, LEIA-PRIMEIRO e DOSSIE; preservar registros antigos e registrar retificações.
- [x] Resolver com o usuário o conflito público: referências a agentes/IDs ficam no diário, D-018. Aplicação pública transferida ao B6/P-017, sem pendência de decisão.
- [x] Executar verificador Claude e verificador independente; 39/39 originais preservados, 716 outros arquivos anteriores inalterados e 34 ausências anteriores mantidas. Links, fontes, IDs e histórico conferidos.
- [x] Mover docs/00_COLAB_IA para _ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA; retirar somente a pasta ativa redundante, sem commit/stage/push.
- [x] Relatório final, LOG incremental e teste de handoff. Próximo agente não deve refazer P-016.

Retomar B0/B1 da P-015 e P-017 conforme dados/decisões já registrados. As 34 ausências preexistentes fora da colaboração, publicações Git, custos e implantação continuam separados. P-013/P-014 têm resultados salvos e fechamento documental pendente. Guia SaaS entregue pelo Claude continua orientação, sem testes externos realizados nesta mescla.

## P-015 — Análise completa Claude frente ao enunciado (concluída, 2026-10-31)

Relatório em `02_TRABALHO/ANALISE_COMPLETA_FASE4_2026-10-31_v01.md`: situação dos 44 requisitos, 112 achados em 10 causas-raiz, plano com datas e decisões do usuário. Somente leitura; nada aplicado. Plano proposto, aguardando decisões e autorizações:

- [ ] B0 (31/10–01/11): ignorar o arquivo de 156 MB (F-024); decidir as 34 deleções; commits curados e push da dev (com autorização); corrigir o lint Python do CI (CIC-02); configurar e testar PagerDuty (Events API v2), Slack (webhook) e a license key do New Relic.
  - Nota 2026-11-01 11:07 (Claude): B0 ainda não iniciado; aguarda autorização de Git, destino das 34 deleções, F-024 e créditos. Docker Desktop parado em 01/11 (necessário para o B1). Nenhuma alteração de código ou na AWS desde a P-015.
- [ ] B1 (01–02/11): E1 externa, ou seja, trace e Service Map no New Relic a partir do Compose, sem AWS.
- [ ] B2 (02–04/11):
  - Terraform: imports.tf, OIDC false, description da policy, tfvars e self-healing (role e access entry).
  - GitOps: OTEL_*, ignoreDifferences e gitops/observability/ (charts, dashboard, alerta, contact points).
  - Falha proposital e self-healing.yml.
- [ ] B3 (05–06/11): plan sem destroy/replace e apply da base; merge para a main; apply de cluster e k8s; stack no ar.
- [ ] B4 (07–09/11): cadeia falha → Firing → PagerDuty → Slack → self-healing, gravada até 10/11, antes do fim do trial.
- [ ] B5 (10–12/11): vídeo de até 25 min; destroy depois da gravação.
- [ ] B6 (13–16/11): relatório PDF, documentação, merge final, acesso do avaliador e submissão até 17/11.

## P-014 — Auditoria independente Codex para comparação em 2026-10-30 19:00 (em andamento)

- [x] Retomar registros Claude/Codex, fixar snapshot e inventário; preservar código e materiais.
- [x] Reler enunciado integral e conferir matriz dos 42 obrigatórios com evidência por página.
- [ ] Revisar fontes/configurações/documentação fora de services/**, classificar cobertura de materiais, histórico, gerados e dependências.
- [x] Executar verificações locais pertinentes sem instanciar serviços, acessar segredos ou modificar infraestrutura.
- [ ] Catalogar achados com severidade, caminho/linha, reprodução, impacto, recomendação/aceite e relação com achadosClaude.
- [ ] Consolidar lacunas FIAP, roteiro de conclusão, resumo para comparação e verificar handoff/preservação.

Saídas em `02_TRABALHO/auditoria-codex-2026-10-30_v01/`. Análise de boas práticas, sem aplicar correções nesta rodada. Não auditar código dos cinco serviços; resultados anteriores desses serviços serão apenas evidência histórica identificada. Não criar automação de19h nem mensagem externa. Datas/fontes e incertezas explícitas.

## P-013 — Executar etapas 8 e 9 (em andamento, 2026-10-28)

- [ ] Etapa8: conferir identidade/região, cinco ECR, role/policy/anexo/OIDC e três Variables GitHub; registrar divergências.
- [ ] Etapa9: corrigir trust Terraform para subject imutável e main, mantendo parametrização e documentação coerentes.
- [ ] Verificar fmt/validate, semântica de trust/permissões e correspondência com a configuração remota; preservar materiais/alterações anteriores.
- [ ] Relatório por etapa, LOG/DECISOES/DOSSIE e teste de handoff.

Auditoria Claude em 2026-10-28 15:11 (sem alterar as caixas do Codex): as evidências mostram etapa 8 executada (34/34 checks em `correspondencia-aws-github.json`) e etapa 9 aplicada no disco (8/8 testes offline do trust; `terraform fmt` aprovado). Falta somente o fechamento documental. Achados F-024 (arquivo de 156 MB não ignorado pelo Git), F-025 (trabalho desde 3b21e65 não comitado) e F-026 (créditos/plano da conta nova não verificados; nuance do Free Tier) no LOG.

Autorização direta do usuário: consultas AWS/GitHub somente leitura e edição local na dev. Sem mutações remotas, backend real, import/state, plan real/apply, commit/push/PR/main. Saídas em `02_TRABALHO/etapas8-9-2026-10-28_v01/`. Não interromper para pedir autorização já dada.

## P-012 — Orientação para criar role IAM/OIDC pelo console (concluída, 2026-10-28)

- [x] Conferir provedor, nomes, trust e permissões do CI.
- [x] Consultar configuração efetiva do subject no GitHub e registrar F-023.
- [x] Preparar guia e JSONs em [role IAM/OIDC](02_TRABALHO/role-github-oidc-2026-10-28_v01/LEIA-ME.md).
- [x] Verificar políticas/links e fechar handoff.

Atualização em 2026-10-28: usuário informou ter executado o guia até o passo7 (provedor/policy/role, Variables e consultas IAM). Considerar essa preparação concluída por relato; resultados concretos não foram consultados pelo agente nesta sessão, e CI remoto ainda não foi testado. Próxima etapa: reconciliar role/policy/attachment/OIDC e ECR existentes com Terraform, corrigindo F-023 antes do apply. Não pedir que crie a role novamente.

## P-011 — Orientação de criação e acessos das contas (concluída, 2026-10-28)

- [x] Conferir o projeto e pesquisar documentação oficial de AWS, GitHub, New Relic, PagerDuty e Slack.
- [x] Salvar guia com cadastro, permissões, integração, limites e critérios de prontidão.
- [x] Verificar referências, distinção entre orientação e execução e handoff.

Escopo: explicar a preparação das contas; não criar contas, contratar planos, configurar credenciais, implantar infraestrutura ou enviar mensagens. P-003/E1 externa/E2–E7 permanecem pendentes até comprovação. A URL do origin é configuração local, não prova de acesso ao GitHub remoto.

Resultado: [guia de contas e acessos](02_TRABALHO/GUIA_CONTAS_E_ACESSOS_FASE4_2026-10-28_v01.md), com cinco serviços e 20 referências oficiais; cinco links locais conferidos. Preparar usuário/permissões Actions no repo04, conta/chave de ingestão New Relic, serviço/política/routing key PagerDuty e workspace/canal/webhook Slack. Conta AWS exige condições de cobrança, identidade temporária, região/cotas e backend próprios; nova conta não renova elegibilidade Free Tier. Verificar continuidade do PagerDuty Free após trial de 14 dias. [INCERTO] condições reais das contas/integrações e limite exato de apps Slack; conferir na conta quando criada. Nenhuma dessas configurações foi executada por esta orientação. Próximo aceite: E1 externa com Compose → Collector → New Relic, em paralelo a P-003; segredos somente locais/armazenamento apropriado.

## P-009 — Revisão integral frente ao enunciado FIAP (concluída, 2026-10-28)

- [x] Reler o enunciado completo e conferir os 42 obrigatórios, opções e dúvidas (sete páginas lidas/renderizadas em 2026-10-27).
- [x] Revisar aplicações/testes/evidências, Terraform/GitOps/CI e documentação/entrega com análises independentes.
- [x] Consolidar matriz por requisito: fonte, estado comprovado, lacuna e critério de conclusão.
- [x] Verificar inventário/preservação, consistência das evidências/IDs/links, registrar achados e handoff.

Escopo desta revisão: inspeção e validações locais necessárias; relatórios em 02_TRABALHO. Sem implementar a stack, corrigir código, executar AWS, publicar Git, enviar telemetria/incidentes ou repetir laboratórios já comprovados sem necessidade. Alterações anteriores e materiais preservados.

Resultado: [revisão consolidada](02_TRABALHO/REVISAO_GERAL_FASE4_2026-10-28_v01.md), matriz JSON e três pareceres setoriais (aplicações/infra de 28; documentação de 27). Os 42 IDs têm página/trecho, evidência e aceite:2 comprovados localmente (02/13), 10 parciais, 28 pendentes e 2 a confirmar. Não é percentual de nota. Catálogo/espelho antigos preservados como fonte normativa; esta matriz é o retrato de execução. Verificação final:42 trechos encontrados no PDF, 37 links dos novos relatórios, 205 arquivos e 28 fontes do ensaio íntegros, 39 protegidos/33 exclusões anteriores preservados. Dev/HEAD/main e fonte03 intactos. Não repetir P-009 sem mudança de escopo/evidência.

## P-010 — Achados da revisão para tratar na implementação (pendente, 2026-10-28)

- [ ] F-023 (descoberto em 2026-10-28): ajustar trust OIDC no Terraform ao subject imutável efetivo confirmado por GET GitHub: repo:fiap-devops-arqcloud-2026@287716251/tech-challenge-04@1373159817. Padrão atual sem IDs não corresponde. Guia P-012 propõe main, alinhada aos jobs de publicação; IaC ainda usa curinga de contextos no padrão antigo. Não aplicar IaC antiga sobre role manual correta. Inventariar/importar recursos criados pelo usuário antes de apply. Evidência em role-github-oidc-2026-10-28_v01/verificacao-oidc.json.

- [ ] F-017: definir/corrigir a distinção entre regra 404 e falhas401/500/timeout do targeting; sonda isolada27 confirmou HTTP 200/result=true e Rule:null no cache. Evitar que indisponibilidade vire liberação de flag. Criar regressões da política escolhida.
- [ ] F-018: distinguir chave inválida de falha operacional do banco auth ou definir sinal de alerta que detecte ambas; código/teste atual devolve 401 para qualquer erroSQL. Não presumir que só5xx capture o incidente.
- [ ] F-019: incluir Collector/stack e endpoint/configuração OTel nos workloads Kubernetes; publicar imagens instrumentadas não ativa o SDK sozinho. Vinculado a E 2/E 3 e REQ-OBR-06–11/14–15/20.
- [ ] F-020: integrar a prova OTel ao CI como melhoria recomendada; atualmente Compose Integration chama apenas test-compose.sh. Não é requisito FIAP de usar um script específico.
- [ ] F-021: atualizar o plano/calendário/runbook e critérios de aceite, preservando versões; contemplar bootstrap ArgoCD, schemas/seed, teste funcional e acionamento do responsável. Corrigir dois links históricos quando revisar esses documentos.
- [ ] F-022: reexecutar DevSecOps sobre artefatos finais e revisar exceções Trivy cuja revisão estava prevista para 2026-10-15. Estado atual dos CVEs não foi consultado nem presumido.

Fonte detalhada: revisão consolidada e pareceres setoriais. São achados/recomendações de implementação, não novas obrigações acadêmicas. Health atual prova vida do processo; não substitui teste funcional. Reprodutibilidade das dependências e dimensionamento2versus3workers também devem ser avaliados antes da implantação. A revisão não autorizou nem aplicou correções, publicação ou deploy. P-003 e E 1 externa/E 2–E 7 seguem pendentes conforme a matriz 42.

## Orientação de avanço — 2026-10-27 (consulta, sem nova implementação)

- Próximo aceite técnico: E1 externa, do Compose já instrumentado ao New Relic, comprovando ingestão, trace e Service Map dos cinco serviços. Conta/chave continuam pendentes conforme última informação do usuário; não repetir P-005/P-008.
- Em paralelo: P-003 (conta, identidade, região, orçamento/cotas e backend próprio) e revisão do calendário/aceites de P-002, preservando o plano v02 histórico. Prazo informado pelo usuário: 2026-11-17; meta interna registrada: 2026-11-12; horário/canal e condição individual continuam incertos.
- Enquanto as contas não estiverem disponíveis, recomendação: preparar métricas/coleta de logs, configurações Helm/GitOps e dashboard; ensaio local com Prometheus/Loki/Grafana é uma opção ainda não implementada. Não comprova métricas/logs do cluster.
- Depois: E2 base → imagens publicadas → cluster → k8s e teste funcional; E3 stack por GitOps; E4 dashboard/alerta/PagerDuty/responsável/Slack; E5 falha controlada e mitigação; E6/E7 evidências dos 42 obrigatórios, vídeo e PDF.
- Esta orientação não autoriza publicação, implantação ou envio de notificações. Seguir trabalhando na dev. Dados sensíveis devem ser configurados localmente, sem chat/Git. Nenhuma decisão de arquitetura foi substituída.

## P-008 — Relatório Terraform e execução dos passos locais (concluído no escopo local, 2026-10-27)

- [x] Concluir explicação leiga/técnica e relatório do Terraform/backend, distinguindo declaração de estado real.
- [x] Passo 1: ensaio integrado aprovado (saída 0, 7 eventos), relatório/resumo registrados antes de avançar.
- [x] Passo 2: cinco serviços + Collector local aprovados; 19 spans com PostgreSQL nos três serviços, HTTP/SQS, logs correlacionados, privacidade e regressão; relatório/resumo salvos.
- [x] Revisão independente, 39 materiais intactos/33 exclusões preservadas, documentação e handoff; laboratório de 12 contêineres/dois volumes encerrado.

Usuário autorizou implementação/testes locais nesta sessão. Sem New Relic por confirmação direta: exportação externa pendente; validar localmente. Sem commit/push/PR/main/AWSreal; fonte03 e materiais intactos. Respeitar alterações anteriores e projeto Docker isolado.

## P-007 — Estudo da Aula 05 CI/CD da Fase 3 (concluído, 2026-10-22)

- [x] Ler PDF integral, figuras/tabelas e conferir conceitos atuais nas fontes primárias.
- [x] Explicar ambientes/módulos/workspaces/branches e alcance dos testes; comparar com as três camadas reais da Fase 3.
- [x] Verificar fonte intacta e registrar handoff em `02_TRABALHO/aula05-terraform-2026-10-22_v01/LEITURA_E_CONFERENCIA.md`.

Limitações não bloqueantes: [INCERTO] exemplo específico de branch/teste na videoaula não acessado e não presente no PDF; aparente inconsistência da linha reutilização na tabela p. 10. Nenhuma implementação ou decisão de criar ambientes foi autorizada por esta consulta.

## P-006 — README: explicações e arquitetura planejada (concluída, 2026-10-22)

- [x] Comparar README, plano e decisões; identificar lacunas de conteúdo.
- [x] Consolidar sinais, funções das ferramentas, execução no cluster/SaaS, conceitos Kubernetes e diagramas.
- [x] Verificar 21 links locais, renderizar/revisar os três diagramas Mermaid e conferir fidelidade às decisões, com revisão independente.
- [x] Atualizar contexto e realizar teste de handoff; 39 materiais preexistentes do 04 intactos por SHA-256 e 33 exclusões anteriores mantidas sem intervenção.

README principal atualizado em 2026-10-22. Evidências em `02_TRABALHO/verificacao-readme-2026-10-22_v01.json` e `02_TRABALHO/resultado-render-readme-2026-10-22_v01.json`. Diagramas são desenho planejado; nenhuma etapa de implantação foi concluída por esta revisão. Sem commit/push/PR.

## P-003 — Provedor escolhido; conta e orçamento pendentes (2026-10-20)

Estado atualizado em 2026-10-28: usuário concluiu guia IAM/OIDC até passo7. Orientações anteriores de role ausente são históricas. Ordem recomendada, ainda sem execução pelo agente:
- [ ] Inventariar ECR/OIDC/role/policy/anexo e conferir conta/região/Variables, aproveitando verificações já feitas pelo usuário.
- [ ] Corrigir F-023 no Terraform local/dev para preservar a trust real com IDs imutáveis e main.
- [ ] Preparar bucket/backend próprios e parâmetros locais; verificar cobrança/orçamento/cotas antes da implantação.
  - 2026-10-28 16:45 (Claude): comandos do bucket entregues ao usuário (namespace regional `-an`, versionado, só TLS; custo estimado abaixo de US$ 0,05). Criação pendente, a cargo do usuário. Contas PagerDuty (trial até cerca de 2026-11-12), Slack e New Relic criadas pelo usuário; conferir a região do New Relic e o que o plano Free do PagerDuty mantém.
  - 2026-10-30 14:45 (Claude): bucket criado pelo usuário (não conferido por mim); falta a policy só TLS e confirmar versionamento/bloqueio público. New Relic na região US. Trial do PagerDuty termina por volta de 2026-11-11 e a linha "Events" do plano Free aparece como "Not included": gravar a evidência alerta → PagerDuty → Slack dentro do trial.
  - 2026-10-30 14:54 (Claude): usuário confirmou o bucket completo. Criados os três `backend.hcl` (ignorados pelo Git). Faltam os `terraform.tfvars` locais e o `init` da base, este com autorização.
- [ ] Inicializar base e incorporar os recursos manuais ao estado, definindo propriedade/reutilização do OIDC.
- [ ] Revisar plan da base quanto a preservação, alterações e custos; aplicação/publicação em etapa posterior autorizada.
A sequência é orientação. Nenhuma operação AWS, importação de estado ou publicação foi autorizada/executada por esta pergunta. CI de imagens exige main; não mudar para dev como atalho. New Relic/Compose pode avançar em paralelo quando conta/chave local estiverem disponíveis.

Complemento em 2026-10-28: explicado onde obter AWS_ROLE_ARN em IAM/CLI; role padrão togglemaster-github-actions e output github_actions_role_arn confirmados no código. Existência, trust OIDC e permissões na conta nova continuam não verificados; ECR não cria essa role automaticamente.

Atualização em 2026-10-28: usuário informou nova conta criada e login CLI realizado; está preparando ECR pelo console. Identidade, região, créditos/cobrança e recursos não foram verificados por ferramentas. Antes do Terraform, inventariar ECR/OIDC/role existentes e importar recursos criados manualmente ao estado correto. O registry usa apenas conta/região; CI espera Variables AWS_REGION/ECR_REGISTRY/AWS_ROLE_ARN. Conta/login informados não comprovam backend, role OIDC ou CI remoto.

Orientação em 2026-10-28: explicado como trocar o perfil AWS CLI default ou usar perfil nomeado e confirmar Account/Arn por STS. Nenhum comando AWS foi executado e a identidade real continua não confirmada. Depois da troca, alinhar expected_aws_account_id, backend e variáveis GitHub; não reutilizar estado da conta anterior.

- [x] Provedor: manter AWS, conforme resposta direta do usuário em 2026-10-20. Avaliação Azure arquivada como referência; não executar migração Azure.
- [ ] Confirmar conta efetivamente disponível e condições de cobrança. Outra conta do mesmo cliente não renova elegibilidade Free Tier, conforme fontes oficiais de 2026-10-20.
- [ ] Atualizar orçamento e cotas antes da implantação; nenhuma conta/recurso criado nesta análise.

## P-004 — Importação da base da Fase 3 (concluída, 2026-10-20)

- [x] Base fixada em 61008794090f582c098e2edc42041339c556f14c, Fase 3 limpa e somente leitura.
- [x] Checkpoint curado do 04 (`4c76a2d`) e merge dos históricos (`491cd2b`) na branch exata `import-fase3`.
- [x] README/CI/CD/ArgoCD/Terraform ajustados para o repo 04; conta anterior removida das configurações operacionais. Adaptação: `31f92e4`.
- [x] Merge local para dev (`cb81b00`); branch import-fase3 preservada. Main do 04 segue em `003a707`; nenhum push/PR/deploy.
- [x] Preservação SHA-256 dos 39 arquivos preexistentes de docs/enunciado 04 e ausência de perdas no manifesto de 933 arquivos; serviços idênticos à fonte.
- [x] Validações locais de Terraform, GitOps, YAML/gates, builds Go, sintaxe Python, Compose config, guias e links; revisão independente sem achados pendentes.

Resultado detalhado: `02_TRABALHO/RESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md`. Scripts, contexto e entregáveis versionados; renderizações/extrações/caches mantidos localmente e ignorados.

## P-005 — Ensaio integrado local (concluído, revalidado em 2026-10-27)

- [x] Docker Desktop com engine Linux confirmado em 2026-10-22: servidor 29.6.1, contexto desktop-linux. A tentativa de 2026-10-20 havia falhado; esta nova conferência remove o bloqueio da engine, sem comprovar o teste integrado.
- [x] Executar `bash scripts/test-compose.sh` em projeto isolado `tc04-integration`; cinco serviços, autenticação, flags/regras, cache e 7 eventos SQS/DynamoDB via Moto aprovados em 2026-10-22.
- [x] Registrar resultados e encerrar somente os 12 contêineres/dois volumes descartáveis tc04-integration; nenhum recurso desse projeto permaneceu, evidências preservadas.

Não confundir `docker compose config` aprovado ou builds Go aprovados com integração funcional. A base antiga não tinha testes Go; agora são 13 principais + oito subtestes e 20 testes Python. CI remoto não foi executado: não houve push/PR.

## P-002 — Implementação da Fase 4 (plano em 2026-09-23)

- [x] Plano de ação e arquitetura (v02) com seis diagramas — `02_TRABALHO/PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html`
- [x] Conferência em 2026-10-21: os 42 obrigatórios estão alocados em E0–E7; ver `02_TRABALHO/CONFERENCIA_PLANO_FASE4_2026-10-21_v01.md`. Alocação não equivale a implementação ou critérios de aceite completos.
- [ ] Atualizar calendário e estado do plano após a importação; detalhar teste funcional da base no cluster (01–05), conta APM/omissão do 12 na síntese e acionamento do responsável pelo PagerDuty (17).
- [ ] Resolver Q-03 sobre entrega individual/grupo (41) e Q-05/Q-06 sobre horário/canal de submissão (42); manter explícita a origem do prazo informado pelo usuário.
- [ ] E0 — Fundação (parcial): importação concluída; faltam conta/backend/cotas/identidades e contas de observabilidade/incidentes confirmadas
- [ ] E1 — Parcial: instrumentação/Collector local concluídos (19 spans/5 serviços); falta conta/configuração e prova de ingestão/trace/mapa no New Relic.
- [ ] E2 — Plataforma no cluster (3 nós, namespace e Secrets novos)
- [ ] E3 — Stack de observabilidade por GitOps
- [ ] E4 — Dashboard e alerta
- [ ] E5 — Self-Healing
- [ ] E6 — Ensaio e matriz de evidências
- [ ] E7 — Gravação, relatório e entrega (meta 2026-11-12; prazo 2026-11-17)

Perguntas em aberto ao usuário (detalhe na seção "Perguntas em aberto" do plano): crédito AWS esgotado declarado em 2026-10-13 (Billing não consultado); estados próprios da Fase4 definidos (bucket/região reais pendentes); mecanismo da falha proposital; qual serviço o self-healing reinicia; composição do grupo (REQ-OBR-41, Q-03); Grafana/Prometheus/Loki também no Compose; registrar o prazo na Q-05 do README.

## P-001 — Requisitos e guias

- [x] A — README de requisitos (revisado com a auditoria adversarial: 42 REQ-OBR, 2 REQ-BON, 4 SUG, Q-01 a Q-14; coluna "Módulo(s)" preenchida; índice §11 publicado)
- [x] B0 — Análise do modelo de referência
- [x] B1 — 00.Welcome to Observabilidade e Monitoramento (21 KB)
- [x] B2 — 01.Observabilidade e Monitoramento (186 KB; Código Fonte 1 completo, F-004 resolvido)
- [x] B3 — 02.Monitoramento Opensource (74 KB; auditado por aula em 2026-09-17, veredito "Fiel")
- [x] B4 — 03.APM (391 KB, 19 seções, 66 blocos de código)
- [x] B5 — 04.Automação de incidentes (90 KB)
- [x] C — Fechamento: módulos mapeados, índice publicado, espelho regenerado, SHA-256 dos 32 originais conferido, validação sem erros
- [x] V — Verificação final executada no laço principal (72 blocos de código, 253 referências de página, amostragem dirigida de 12 afirmações): 3 âncoras corrigidas, nada inventado. Registro em `02_TRABALHO/verificacoes/verificacao-final-2026-09-21_v01.md`

## Estado dos entregáveis

| Arquivo | Tamanho | Seções | Blocos de código | Validação |
|---|---|---|---|---|
| `docs/requisitos/README.md` | 28 KB | 11 | — | 0 erros |
| `docs/requisitos/REQUISITOS.html` (espelho gerado) | 49 KB | 11 | — | 48 âncoras |
| B1 Welcome | 21 KB | 8 | 0 | 0 erros |
| B2 Observabilidade | 186 KB | 17 | 1 | 0 erros |
| B3 Opensource | 74 KB | 15 | 1 | 0 erros |
| B4 APM | 391 KB | 19 | 66 | 0 erros |
| B5 Incidentes | 90 KB | 17 | 6 | 0 erros |

## Achados

- F-001 a F-007: ver LOG (entradas de 2026-09-16).
- F-008: Atlassian encerrou a venda do OpsGenie em 2025-06-04 e desliga o produto em 2027-04-05; virou a dúvida Q-09 do README. Fato de mercado, não regra da FIAP.
- F-009: guias regenerados em 2026-09-17 apontavam para `REQUISITOS.html` inexistente; resolvido criando o espelho gerado a partir do README.
- F-010: o gerador de fragmentos do módulo Incidentes estava completo desde 2026-09-17 e nunca fora executado; B5 montado em 2026-09-20.
- F-011: dois limites de uso da conta interromperam execuções com subagentes (2026-09-16, 32 agentes; 2026-09-20, 12 agentes). Trabalho inline, aula a aula, gravando cada arquivo assim que fica pronto, é a forma resiliente — foi assim que o B4 saiu.
- F-012: `file://` deixou de abrir no painel do navegador durante a sessão de 2026-09-21; a revisão visual dos guias novos ficou limitada à auditoria estrutural.

## Retomada

1. Trabalhar na `dev` do repo 04. Importação já concluída; não repetir, não alterar a Fase 3. PR/main e push aguardam pedido do usuário.
2. P-005 e P-008 locais concluídas: não repetir implementação/importação. Para reproduzir, usar scripts/test-observability.sh e relatórios de 2026-10-27. Próximo aceite de E1 é New Relic, com chave configurada localmente; métricas e coleta de logs aos backends continuam em E3. Laboratório encerrado, evidências em qa-passos-locais-2026-10-27.
3. Em paralelo, aguardar dados da nova conta; preencher repository variables e configurações locais de backend/tfvars, conferir conta/cotas/orçamento e substituir os marcadores GitOps pelos outputs reais. Confirmar acessos New Relic/PagerDuty/Slack. Não transportar estado/segredos antigos. E2 depende da configuração AWS e da publicação futura autorizada das imagens; seguir base → imagens → cluster → k8s. E3–E7 seguem stack, dashboard/alerta, automação e evidências/entrega.
4. Fontes/guias preservados; validadores agora selecionam só os cinco módulos do 04 pelo inventário original. `docs/00_COLAB_IA` é histórico do 03; contexto vigente está em `00_COLAB_IA` na raiz.
5. Prazo informado pelo usuário: 2026-11-17; o calendário antigo deve ser replanejado. Destruições exigem autorização específica.

## Pendências herdadas da Fase 3 — triagem de 2026-11-01

Levantamento de 2026-11-01 a partir de `docs/00_COLAB_IA/`. Os originais ficam no commit 3b21e65 (`git show 3b21e65:docs/00_COLAB_IA/ARQUIVO`) e no repositório tech-challenge-03. Caminhos "Fonte F3" são relativos a `docs/00_COLAB_IA/`. As linhas de código vêm da consolidação Claude em 2026-11-01; os números mudam conforme as edições. Não são uma nova auditoria dos serviços pelo Codex. A tabela só traz itens que ainda se aplicam ("sim") ou que podem se aplicar ("talvez").

| ID F3 | Pendência | Ainda se aplica? | Ação sugerida | Relação na Fase 4 |
|---|---|---|---|---|
| F3-D-015 | Desvio na topologia dos bancos: 2 RDS e o banco do targeting em StatefulSet, em vez de 3 RDS. O professor aceitou o arranjo em 2026-08-27, para a Fase 3, por causa do limite da conta antiga. Em 2026-09-09 o comprovante escrito não foi localizado. O arranjo continua no código (terraform/README.md:12; terraform/cluster/main.tf:74). Fonte F3: DECISOES.md (170-182); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (28). | sim | Verificar o limite de RDS na conta nova. Se o desvio continuar, justificá-lo no relatório da Fase 4. Nesse caso, registrar a ressalva do aceite verbal ou obter a confirmação do tutor por escrito. | DOC-01, DOC-08, P-003. docs/RELATORIO_DE_ENTREGA.md:41 e :48 (relatório histórico). |
| F3-P-059 | Gerador do PDF do relatório. Os dois geradores da Fase 3 só existem em `_ARQUIVO_MORTO`: gerar-relatorio-pdf_2026-09-11_v00.py (markdown e weasyprint) e build-report-fase3_2026-09-14.py (reportlab, o canônico desde 2026-09-14). As fontes da Fase 3 divergem sobre qual era o canônico. Em 2026-09-15 o reportlab não estava instalado, e o README apontava para um PDF em output/, pasta ignorada (link quebrado no GitHub). Não há gerador em scripts/. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (820-824); _ARQUIVO_MORTO/build-report-fase3_2026-09-14.py (3-21); LOG_DE_TRABALHO.md (196, 201). | sim | Geradores preservados no acervo integral; também recuperar por: `git show 3b21e65:docs/00_COLAB_IA/_ARQUIVO_MORTO/<arquivo>`. Escolher a ferramenta da Fase 4, com uma única fonte de texto, e testá-la cedo. O PDF final vai para uma pasta versionada; nunca linkar output/. | REQ-OBR-32 (relatório em PDF); DOC-01; P-015 B6. |
| F3-P-053 | Encerramento da conta da Fase 3. Inclui desativar usuários IAM e credenciais manuais, que os estados não removem. As camadas foram destruídas em 2026-09-15; restaram F3-P-100 e F3-P-101. Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (208-218); LOG_DE_TRABALHO.md (67-71). | talvez | O usuário confere no console da conta antiga se ainda há custo e desativa as identidades manuais, sem usar essas credenciais no trabalho da Fase 4. No fim da Fase 4, repetir a limpeza na conta nova, conferindo o provedor OIDC antes de excluí-lo. | P-015 B5 (destroy depois da gravação); TFC-05. |
| F3-P-103 | Composição do grupo e acesso do avaliador. Na Fase 3 a confirmação independente não veio, e o [INCERTO] ficou no relatório. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (14); DECISOES.md (15). | sim | Confirmar com o tutor, por escrito, se a entrega é individual ou em grupo, e registrar no LOG com data. Garantir que o avaliador acesse o repositório 04 (privado) antes da submissão. Não copiar a tabela de integrantes da Fase 3. | D-009 (implementação solo) contra REQ-OBR-41 (em grupo) [INCERTO]; Q-03; DOC-08; TFK-11; B6. |
| F3-P-104 | Dados pessoais em material versionado. Um relatório preliminar arquivado traz usuários de Discord, e uma decisão da Fase 3 traz um caminho local com o nome do usuário. docs/RELATORIO_DE_ENTREGA.md (histórico) traz nomes e RMs dos integrantes. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (15). | sim | Na mescla, não copiar esses dados para a pasta vigente. Apagar docs/00_COLAB_IA não limpa o histórico do Git. O usuário decide se aceita o histórico como está, com o repositório privado. Reescrever o histórico só com pedido explícito. | DOC-12. |
| F3-P-105 | Metadado "generated using python-pptx" nas propriedades de docs/apresentacao/ToggleMaster_Fase3.pptx, que continua no repositório (conferido em 2026-11-01). Item opcional. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (16). | talvez | Decidir se a apresentação da Fase 3 fica no repo 04. Conferir metadados de gerador no material novo. | Ligada à regra de documento público, na linha abaixo. |
| Regra F3 (sem ID) | Documento público sem IA, assistentes, o nome 00_COLAB_IA ou códigos internos (D-, F-, P-, O-, R-, S-). O README da Fase 4 cita Codex (README.md:5) e D-009, D-012 e D-014 (README.md:14-16, 43, 184-186 e 226). terraform/README.md, gitops/README.md e observability/README.md também citam esses termos. O CLAUDE.md está versionado na raiz, contra 00_COLAB_IA/ORGANIZACAO_DE_PASTAS.md:18. Fonte F3: INSTRUCOES_ASSISTENTES.md (39); LEIA-PRIMEIRO.md (28). | talvez | Resolvido pelo usuário em D-018: retirar referências internas dos documentos públicos na revisão B6/P-017. Manter diário e CLAUDE.md interno; não reescrever histórico. | P-015 B6; XCL-04. |
| F3-P-110 | Comentários desatualizados nos workflows reutilizáveis. Um fala em "git pull --rebase", mas o job refaz fetch e reset em laço. Outro diz "única permissão de escrita", mas jobs sem bloco permissions herdam o teto do chamador. Ainda em .github/workflows/_ci-go.yml:499 e :524 e em _ci-python.yml:529 e :554. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (24). | sim | Corrigir junto com F3-P-111 na dev. Levar à main só com a role do CI e o ECR da conta nova prontos (F3-P-140). | CIC-03, CIC-16. |
| F3-P-111 | Falta declarar permissions por job em build, lint, sast e sca. O topo dos workflows de serviço dá id-token: write e contents: write (ex.: .github/workflows/analytics-service.yml:76-82). Só image e gitops redefinem as permissões (_ci-go.yml:335 e :497). Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (25). | sim | Declarar contents: read nos jobs de verificação. Aplicar a mesma regra ao workflow de self-healing. | CIC-03. |
| F3-P-112 (inclui P-024) | READMEs de services/ herdados da Fase 2: Go 1.21, Python 3.9, us-east-1 e chaves AWS estáticas. Em 2026-11-01: services/analytics-service/README.md:16-17, :52 e :58; services/evaluation-service/README.md:57 e :60; services/flag-service/README.md:11. A região do projeto é us-east-2. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (26); INSTRUCOES_ASSISTENTES.md (116); _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (160-161, 414). | sim | Reescrever junto com a documentação da instrumentação OTel, sem chaves estáticas e com a região certa. Qualquer edição em services/&lt;svc&gt;/** dispara o pipeline e, na main, tenta OIDC. Por isso, agrupar com outra mudança do serviço. | DOC-07; CIC-16. |
| F3-P-113 | Flask, gunicorn e setuptools sem versão fixa em services/analytics-service/requirements.txt (:1, :2 e :5). As dependências OTel do mesmo arquivo já estão fixadas. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (27). | sim | Fixar versões compatíveis com Python 3.12. Depois, rodar de novo o SCA e o ensaio local. | CIC-11; D-016. |
| F3-P-114 | PyYAML==6.0.1 em services/flag-service/requirements.txt:8. É sobra da demonstração de CVE; o serviço não usa YAML. As fontes divergem: o guia de 2026-09-11 mandava remover, e o plano de 2026-09-15 mandava manter até a Cena 6. O Apêndice B do guia histórico usa essa linha (docs/GUIA_DE_REPRODUCAO.md:746-841). Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (28); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (980-982); _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (414-415). | sim | Decidir se a demonstração de CVE entra no vídeo da Fase 4. Se não entrar, remover a dependência. A mudança gera imagem nova na main. | Sem achado P-015 específico. |
| F3-P-115 | Comentários ainda citam o ESO e o externalsecret.yaml: gitops/base/auth-service/deployment.yaml:67-68, gitops/base/evaluation-service/deployment.yaml:61 e gitops/base/flag-service/deployment.yaml:51. Os Secrets vêm de terraform/k8s/secrets.tf. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (29). | sim | Corrigir quando os deployments receberem as variáveis OTEL_*. | GIT-08, GIT-02. |
| F3-P-120 | terraform/terraform.tfvars.example:41 traz enable_nat_gateway = false, ao contrário do padrão true. Copiado sem ajuste, quebra uma recriação do zero: os pods ficam em ImagePullBackOff. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (35); INSTRUCOES_ASSISTENTES.md (129). | sim | Corrigir o exemplo ou garantir true no tfvars local da base antes do primeiro apply. | XCL-03, TFK-10; B2. |
| F3-P-121 | Comentários sobre EKS 1.31, "repositório privado" e "evita o provider helm", além da ordem das camadas sem a k8s: terraform/modules/eks/main.tf:73-74, terraform/cluster/main.tf:55, terraform/modules/eks/variables.tf:24 e terraform/cluster/outputs.tf:27. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (36). | sim | Corrigir antes do apply, junto com a revisão de versão do EKS (F3-P-131). | TFC-03, TFC-06. |
| F3-P-122 | Comentário cita o GUIA-AWS.md da Fase 2, que não existe (terraform/modules/messaging/main.tf:90). Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (37). | sim | Remover a referência. | CIC-16. |
| F3-P-123 | ecr_image_tag_mutability = MUTABLE (terraform/variables.tf:143; terraform/terraform.tfvars.example:63). Os ECR da conta nova foram criados à mão, e o inventário autenticado de 2026-10-28 confirmou MUTABLE; revalidar antes da adoção pelo Terraform. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (38). | sim | Decidir entre MUTABLE e IMMUTABLE antes do import dos ECR, para o plan não propor mudança inesperada. | TFB-01, XCL-03. |
| F3-P-124 (inclui P-049/F-048) | scripts/security-check.sh desatualizado. A exclusão ':!*.example.*' não cobre .env.example (:51). A regra de conta legada só procura o ID da Fase 2 (:70-78). Um comentário traz o ID da Fase 3 (:11). O script não cobre os segredos da Fase 4. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (39); LOG_DE_TRABALHO.md (251). | sim | Bloquear &lt;CONTA_FASE3&gt; sem escrever o ID em claro e tirá-lo do comentário. Cobrir chaves de New Relic, PagerDuty e Slack. Avaliar varredura de segredos no CI. | CIC-05, XCL-14. |
| F3-P-130 | Revisar as 3 exceções do perl-base no .trivyignore. A revisão estava marcada para 2026-10-15 e venceu (.trivyignore:58). As imagens Python ganharam dependências OTel. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (45); INSTRUCOES_ASSISTENTES.md (105). | sim | Rodar o Trivy, na versão usada pelo CI, sobre as imagens finais. Manter ou remover cada exceção, com nova data (exp: na própria linha). | CIC-08; F-022. |
| F3-P-131 (inclui P-050/F-049) | Versão do EKS e estimativa de custo. Fora do suporte padrão, o plano de controle custa 6 vezes mais: US$ 0,60/h contra US$ 0,10/h (registro de 2026-09-15). O fim do suporte padrão do 1.34 diverge entre as fontes: 2026-12-01 (Fase 3) ou 2026-12-02 (P-015, TFC-03) [INCERTO]. As duas datas ficam depois da entrega. A estimativa de 2026-09-11 (US$ 0,385/h; US$ 281,03/mês) não inclui a observabilidade. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (46); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (1589-1592). | sim | Antes do apply, rodar `aws eks describe-cluster-versions` e avaliar upgrade_policy STANDARD. Refazer a estimativa e o print na conta nova, com data. | TFC-01, TFC-03, XCL-10, DOC-01. |
| F3-P-132 | Cerca de 30 dias depois de cada run [INCERTO], o GitHub deixa de aceitar gh run rerun dos runs de push na main. workflow_dispatch não publica imagens. Fonte F3: PENDENCIAS_E_PROXIMOS_PASSOS.md (47); INSTRUCOES_ASSISTENTES.md (123). | talvez | Publicar as imagens por commit na main do repo 04 (B3), com autorização. | CIC-13, GIT-03. |
| F3-P-140 | Ordem de merge na main. Mudanças em services/** ou .github/workflows/** que chegam à main antes da role OIDC e do ECR geram runs vermelhos. Em 2026-09-14 o flag-service falhou ao assumir a role. Na Fase 4, a role foi criada à mão e conferida no inventário P-013 de 2026-10-28, e o CI remoto não foi testado. Fonte F3: LOG_DE_TRABALHO.md (14, 107); DECISOES.md (12, 24). | sim | Levar à main só depois de conferir role, ECR e Variables. É uma ordem de execução, não uma proibição de editar na dev. | XCL-08; B3. |
| F3-P-040 (inclui F-047) | Preencher o overlay prod depois do apply: REDIS_URL, AWS_SQS_URL, ARNs de IRSA e imagens. Hoje os valores são sentinelas (gitops/overlays/prod/patches/endpoints.yaml:31, :39 e :49). A hipótese sobre o identificador do ElastiCache não foi confirmada. Fonte F3: LOG_DE_TRABALHO.md (250, 288); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (260-285). | sim | Substituir pelos outputs reais, conforme gitops/README.md:24-36, e conferir a cada recriação. | GIT-03, TFK-03. |
| F3-P-041 (inclui P-042 e P-047/F-044) | Ensaio completo com o cluster no ar: apply das camadas, schemas de auth e flag nos RDS, seed (chave, SERVICE_API_KEY, flag e regra), ArgoCD Synced/Healthy e uma tag nova sincronizada. RDS novos nascem vazios. Schemas e seed manuais levavam cerca de 15 min por sessão. Fonte F3: LOG_DE_TRABALHO.md (271, 305); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (331-345); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (1003-1012). | sim | Incluir no runbook da Fase 4 e avaliar um Job ou script. No primeiro apply, medir o tempo de criação da base do zero. Esse tempo nunca foi medido; o guia reservava 10 min. | B3, B4, DOC-02; F-021. |
| F3-P-046 (F-043) | Instalar o ArgoCD (CRD) separado da criação da Application: etapa A com -target=helm_release.argocd e etapa B em seguida. O procedimento histórico resolve isso (docs/GUIA_DE_REPRODUCAO.md:446-452), mas nunca foi ensaiado na conta nova. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (42-48). | sim | Manter as duas etapas no runbook e ensaiá-las no B3. | TFK-05. |
| F3-P-048 (F-046) | Dono único da SERVICE_API_KEY, para que apply ou restart não desfaçam o seed. O desfecho na Fase 3 não foi confirmado [INCERTO]. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (58-70); _ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md (39, 51). | sim | Definir quem grava a chave (Terraform ou passo manual). Testar o reinício do evaluation depois do seed. O self-healing reinicia pods, e com a chave provisória o /evaluate responde 502. | CIC-01, GIT-07. |
| F3-P-052 (inclui P-051) | O robô do CI faz push de tags direto na main, e o GitHub não tinha proteção de branch. A disciplina dev → PR → main era só processual. Foi encerrada na Fase 3 como exceção intencional (F3-D-021). O push na main continua em .github/workflows/_ci-go.yml:606 e _ci-python.yml:636. Fonte F3: DECISOES.md (65-109); LOG_DE_TRABALHO.md (265, 284). | sim | Decidir a política (push do robô ou PR de promoção) antes de ativar a proteção e antes de criar o workflow de self-healing. Não alterar regras remotas sem autorização. | CIC-07, XCL-08, CIC-01. |
| F3-P-034 | Runbook de sessão e de custo: subir, semear, gravar e derrubar a camada cara. Não há roteiro vigente para a conta nova. O guia importado é da Fase 3 e tem comandos incompatíveis com o código atual. Fonte F3: LOG_DE_TRABALHO.md (389); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (7). | sim | Escrever o runbook da Fase 4 com a stack de observabilidade, no formato que funcionou em 2026-09-15. Medir tempos e custos em vez de copiá-los. | DOC-02; F-021. |
| F3-F-014 | ID da conta no nome do bucket e em arquivo versionado. Na Fase 3 foi um risco aceito, mitigado com repositório privado. Na conta nova está mitigado: bucket e região ficam em backend.hcl ignorado (terraform/README.md:17). O ID da Fase 3 ainda aparece em docs/GUIA_DE_REPRODUCAO.md (10 ocorrências), em scripts/security-check.sh:11 e em cópias em 00_COLAB_IA/_ARQUIVO_MORTO/FASE3_BASE_6100879 e 02_TRABALHO. Fonte F3: LOG_DE_TRABALHO.md (423); _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (416). | talvez | Decidir antes de dar acesso ao avaliador. Avaliar a troca do ID por marcador no guia histórico. Remover docs/00_COLAB_IA reduz as ocorrências, mas não limpa o histórico. | DOC-12, XCL-14. |
| F3-S-03 (S-03, S-04, S-07, R-08) | Sugestões não implementadas na Fase 3: scan de IaC (Checkov, tfsec ou Trivy config), Prowler, CloudTrail e logs do EKS, SonarCloud. Até onde foi conferido, o enunciado da Fase 4 não as exige. Fonte F3: _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (99, 103, 112-116). | talvez | Avaliar só o que tem justificativa direta (scan de IaC e logs do plano de controle do EKS). Não inflar o escopo. | CIC-06, TFC-07. |

Não se aplicam à Fase 4:

- F3-P-100: excluir o bucket de estado da Fase 3 (togglemaster-tfstate-&lt;CONTA_FASE3&gt;-us-east-2-an).
- F3-P-101: excluir a VPC da Fase 2 que sobrou na conta antiga.
- Os dois são da conta antiga, proibida na Fase 4. Ficam como limpeza e possível custo, a critério do usuário e fora deste repositório. A exclusão do bucket é permanente.
- F3-P-102: vídeo e relatório da Fase 3. Não preencher o relatório histórico. Lição para a Fase 4: incluir no relatório o link do vídeo testado em aba anônima.
- F3-P-074: a referência histórica ao bootstrap não deve reabrir a criação do bucket novo. Na Fase 4 ele foi confirmado completo pelo usuário em 2026-10-30; proteções, nome e tags ainda não foram consultados pelo agente nesta retomada. Backend local existe; init/import/apply não executados.
- F3-P-035/P-036: addons, StorageClass gp3 e instalação do kustomize standalone para editar a tag existem no código. Isso não resolve o gate de renderização dos manifests no CI (F-029/CIC-09), que permanece pendente.
- F3-F-050: conflito sobre o destroy da camada k8s, já resolvido em terraform/README.md:65.
- F3-R-04: testes unitários, superado. Em 2026-10-27 foram aprovados 13 testes Go principais, oito subtestes e 20 testes Python.
- F3-RELATORIO-9: badge do Google Cloud Skills Boost, sem equivalente na Fase 4.
## P-017 — Aplicar política pública e retificações da mescla (pendente, 2026-11-01)

- [x] Resolver conflito de autoria/IDs internos: usuário escolheu diário interno; decisão D-018.
- [ ] Na revisão B6, retirar referências a assistentes e IDs internos dos READMEs/documentos públicos vigentes, preservando histórico e créditos/licenças legítimos.
- [ ] Corrigir justificativas nos comentários de Terraform: use_lockfile existe desde 1.10.0; >=1.11.0 é escolha do projeto. Não é necessário baixar a restrição de versão. Bucket Key não é recurso SSE-S3.
- [ ] Antes do deploy, escolher versão mantida e corrigida do ArgoCD; 7.7.11 → appVersion v2.13.2 e CVE-2025-55190 confirmados por fontes oficiais em 2026-11-01. Não houve teste de exploração nem implantação nesta retomada (TFK-02).
- [ ] Revisar runbook futuro: diagnóstico antes de apagar recursos; plano salvo com aprovação antes de aplicar; não imprimir prefixos de chaves nem transportar DATABASE_URL em argumentos visíveis. Diferenciar intervalo de reconciliação de prazo garantido.

Fontes e rastreabilidade: [relatório](02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md) e [índice completo](02_TRABALHO/mescla-colab-fase3-2026-11-01_v01/INDICE_RASTREABILIDADE_2026-11-01_v01.md). São melhorias/retificações, não novas exigências da FIAP. 39 registros de pendências herdadas incluem duplicatas e itens fora da Fase 4; não somá-los aos 42 requisitos.
