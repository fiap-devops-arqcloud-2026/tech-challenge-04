# Pendências e progresso

TL;DR: importação com histórico concluída e mesclada na dev em 2026-10-20; Fase 3 e materiais do 04 preservados. README/CI/ArgoCD adaptados. Main/PR/push intactos. Conta AWS e integração Docker pendentes; E1 de observabilidade ainda não iniciada.

Última atualização: 2026-10-21, Codex.

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

## P-005 — Ensaio integrado local (pendente de Docker)

- [ ] Iniciar Docker Desktop com engine Linux funcional. A tentativa nesta sessão terminou após 50 s sem engine; serviço consultado parado.
- [ ] Executar `bash scripts/test-compose.sh` em projeto isolado `tc04-integration`; conferir os cinco serviços, autenticação, flags/regras, cache e fluxo SQS/DynamoDB via Moto.
- [ ] Registrar resultado e encerrar somente os contêineres/volumes descartáveis desse teste.

Não confundir `docker compose config` aprovado ou builds Go aprovados com integração funcional. Go informou ausência de testes unitários; CI remoto também não foi executado porque não houve push/PR.

## P-002 — Implementação da Fase 4 (plano em 2026-09-23)

- [x] Plano de ação e arquitetura (v02) com seis diagramas — `02_TRABALHO/PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html`
- [x] Conferência em 2026-10-21: os 42 obrigatórios estão alocados em E0–E7; ver `02_TRABALHO/CONFERENCIA_PLANO_FASE4_2026-10-21_v01.md`. Alocação não equivale a implementação ou critérios de aceite completos.
- [ ] Atualizar calendário e estado do plano após a importação; detalhar teste funcional da base no cluster (01–05), conta APM/omissão do 12 na síntese e acionamento do responsável pelo PagerDuty (17).
- [ ] Resolver Q-03 sobre entrega individual/grupo (41) e Q-05/Q-06 sobre horário/canal de submissão (42); manter explícita a origem do prazo informado pelo usuário.
- [ ] E0 — Fundação (parcial): importação concluída; faltam conta/backend/cotas/identidades e contas de observabilidade/incidentes confirmadas
- [ ] E1 — Instrumentação local (Compose + Collector local → New Relic)
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
2. Aguardar dados da nova conta; preencher repository variables e configurações locais de backend/tfvars, conferir conta/cotas/orçamento e substituir todos os marcadores GitOps pelos outputs reais. Não transportar estado/segredos antigos.
3. Resolver P-005 e iniciar E1 (instrumentação/Collector local/New Relic). Ainda não foi implementada observabilidade nem Self-Healing nesta importação.
4. Fontes/guias preservados; validadores agora selecionam só os cinco módulos do 04 pelo inventário original. `docs/00_COLAB_IA` é histórico do 03; contexto vigente está em `00_COLAB_IA` na raiz.
5. Prazo informado pelo usuário: 2026-11-17; o calendário antigo deve ser replanejado. Destruições exigem autorização específica.
