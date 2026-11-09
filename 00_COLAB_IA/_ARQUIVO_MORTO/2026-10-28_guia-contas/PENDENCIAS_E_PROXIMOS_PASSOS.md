# Pendências e progresso

TL;DR: importação com histórico concluída e mesclada na dev em 2026-10-20; Fase 3 e materiais do 04 preservados. README/CI/ArgoCD adaptados. Main/PR/push intactos. Conta AWS pendente; integração e instrumentação locais aprovadas em 2026-10-27; APM externo e cluster pendentes.

Última atualização: 2026-10-28, Codex.

## P-009 — Revisão integral frente ao enunciado FIAP (concluída, 2026-10-28)

- [x] Reler o enunciado completo e conferir os 42 obrigatórios, opções e dúvidas (sete páginas lidas/renderizadas em 2026-10-27).
- [x] Revisar aplicações/testes/evidências, Terraform/GitOps/CI e documentação/entrega com análises independentes.
- [x] Consolidar matriz por requisito: fonte, estado comprovado, lacuna e critério de conclusão.
- [x] Verificar inventário/preservação, consistência das evidências/IDs/links, registrar achados e handoff.

Escopo desta revisão: inspeção e validações locais necessárias; relatórios em 02_TRABALHO. Sem implementar a stack, corrigir código, executar AWS, publicar Git, enviar telemetria/incidentes ou repetir laboratórios já comprovados sem necessidade. Alterações anteriores e materiais preservados.

Resultado: [revisão consolidada](02_TRABALHO/REVISAO_GERAL_FASE4_2026-10-28_v01.md), matriz JSON e três pareceres setoriais (aplicações/infra de 28; documentação de 27). Os 42 IDs têm página/trecho, evidência e aceite:2 comprovados localmente (02/13), 10 parciais, 28 pendentes e 2 a confirmar. Não é percentual de nota. Catálogo/espelho antigos preservados como fonte normativa; esta matriz é o retrato de execução. Verificação final:42 trechos encontrados no PDF, 37 links dos novos relatórios, 205 arquivos e 28 fontes do ensaio íntegros, 39 protegidos/33 exclusões anteriores preservados. Dev/HEAD/main e fonte03 intactos. Não repetir P-009 sem mudança de escopo/evidência.

## P-010 — Achados da revisão para tratar na implementação (pendente, 2026-10-28)

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
