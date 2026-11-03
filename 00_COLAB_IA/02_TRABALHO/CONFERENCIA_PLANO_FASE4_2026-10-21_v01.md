# Conferência do plano de ação — Tech Challenge Fase 4

TL;DR: existe plano E0–E7 com alocação dos 42 requisitos obrigatórios. O escopo está previsto, mas faltam atualização do calendário e detalhamento de alguns critérios de aceite. Alocação no plano não comprova implementação ou aceitação das dúvidas pela FIAP.

Última atualização: 2026-10-21, Codex; revisão independente pelo agente audit_requirements.

## Verificação realizada

- [x] Ler protocolo, pendências, LOG e decisões pertinentes.
- [x] Conferir os 42 IDs do README contra as etapas do plano.
- [x] Revisar independentemente as condições de conclusão e dúvidas abertas.
- [x] Registrar limites e próximos passos sem alterar o plano ou o código.

Fontes locais conferidas em 2026-10-21: [plano v02](PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html#plano), [requisitos](../../docs/requisitos/README.md), [pendências](../PENDENCIAS_E_PROXIMOS_PASSOS.md) e decisões D-009/D-014. A análise compara estes documentos; não constitui nova auditoria integral do PDF ou teste da aplicação.

## Alocação no plano

IDs abreviados abaixo mantêm o prefixo `REQ-OBR-`.

| Etapa | Trabalho previsto | IDs alocados |
|---|---|---|
| E0 | Repositório, contas e inventário | 01–05, 12, 17, 18 |
| E1 | Instrumentação, tracing e mapa dos serviços | 13–15, 21 |
| E2 | Base anterior funcionando no cluster | 01–05 |
| E3 | Prometheus, Loki, Grafana e Collector por GitOps | 06–09, 11, 20 |
| E4 | Dashboard, alerta, incidente e ChatOps | 10, 16–18 |
| E5 | Automação de Self-Healing | 19, 22 |
| E6 | Ensaio e matriz de evidências | 23 |
| E7 | Vídeo, relatório e submissão | 24–42 |

A união dos IDs corresponde aos 42 obrigatórios do README, sem ID inexistente. Referência: plano, linhas 969–1077. A frase-síntese da linha 1077 omite o número 12, mas a E0 o inclui expressamente na linha 979 e prevê criar a conta New Relic na linha 975. A matriz individual de evidências ainda é tarefa futura da E6.

## Refinamentos antes de considerar o plano fechado

1. **REQ-OBR-01–05:** E2 usa pods Running e ArgoCD Synced como condição de conclusão (linha 1005). Acrescentar teste funcional integrado no cluster; esses estados isolados não demonstram a base funcionando.
2. **REQ-OBR-12:** corrigir a omissão na frase-síntese e confirmar a conta APM disponível e o atendimento à orientação educacional do enunciado; Q-04 continua aberta. New Relic já foi escolhido pelo usuário.
3. **REQ-OBR-17:** E4 prevê incidente aberto e notificação separada no Slack (linhas 1029–1032), mas não explicita configuração e teste do acionamento do responsável/time pelo PagerDuty. Tornar esse teste um critério de aceite.
4. **REQ-OBR-41 — [INCERTO]:** confirmar aceitação de entrega individual ou composição do grupo. Implementação solo é decisão do usuário; aceitação pela FIAP continua sendo Q-03 (plano, linhas 1130 e 1143).
5. **REQ-OBR-42 — [INCERTO]:** 2026-11-17 foi informado pelo usuário; horário final, canal e procedimento oficial de submissão continuam pendentes (Q-05/Q-06). Atualizar o calendário iniciado em 2026-09-23, considerando a situação de 2026-10-21.

Também permanecem decisões técnicas do cenário de falha e alvo do reinício (linhas 1141–1142), além das dúvidas Q-13 sobre usernames e Q-14 sobre o critério de alerta inteligente. Registrar as respostas e critérios de demonstração ao detalhar E4–E7.

## Estado e retomada

P-004 concluída: importação na dev. E0 permanece parcial; dados da nova conta AWS e ensaio integrado Docker pendentes. E1–E7 não foram declaradas concluídas. O plano continua sendo referência arquitetural, com calendário e alguns pontos de configuração anteriores à importação; LOG/PENDENCIAS atuais prevalecem para o estado de execução.

Nesta conferência não houve alteração do plano, implementação, commit, push, PR ou operação de nuvem. Foram observadas exclusões locais preexistentes de 33 materiais históricos importados da Fase 3; não foram restauradas, alteradas ou incluídas em commit. Não atribuir essas alterações a esta conferência.
