# Pendências e progresso

TL;DR: P-001 concluída (requisitos e guias). P-002 é a implementação da Fase 4: plano e arquitetura entregues em `02_TRABALHO/PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html`; nenhuma etapa executada ainda. Entrega em 2026-11-17.

Última atualização: 2026-09-24, Claude (Opus 5.5).

## P-002 — Implementação da Fase 4 (plano em 2026-09-23)

- [x] Plano de ação e arquitetura (v02) com seis diagramas — `02_TRABALHO/PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html`
- [ ] E0 — Fundação: inventário AWS somente leitura, migração do código para o 04, contas New Relic/PagerDuty/Slack, token do GitHub
- [ ] E1 — Instrumentação local (Compose + Collector local → New Relic)
- [ ] E2 — Plataforma no cluster (3 nós, namespace e Secrets novos)
- [ ] E3 — Stack de observabilidade por GitOps
- [ ] E4 — Dashboard e alerta
- [ ] E5 — Self-Healing
- [ ] E6 — Ensaio e matriz de evidências
- [ ] E7 — Gravação, relatório e entrega (meta 2026-11-12; prazo 2026-11-17)

Perguntas em aberto ao usuário (detalhe na seção "Perguntas em aberto" do plano): crédito AWS restante; estratégia de estado do Terraform após a migração; mecanismo da falha proposital; qual serviço o self-healing reinicia; composição do grupo (REQ-OBR-41, Q-03); Grafana/Prometheus/Loki também no Compose; registrar o prazo na Q-05 do README.

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

1. Ler os arquivos em `02_TRABALHO/verificacoes/`; aplicar cada achado confirmado no fragmento correspondente (`02_TRABALHO/fragmentos/<modulo>/`) e remontar com `montar-guia-2026-09-16_v01.py <config.json>`.
2. Revalidar: `python -X utf8 validar-guias-2026-09-16_v01.py` (Python do runtime Codex; o do PATH não tem pypdfium2).
3. Se o navegador permitir, abrir os cinco guias em tela ampla e estreita e conferir ausência de rolagem horizontal.
4. Sem commit/push — o usuário não autorizou.
