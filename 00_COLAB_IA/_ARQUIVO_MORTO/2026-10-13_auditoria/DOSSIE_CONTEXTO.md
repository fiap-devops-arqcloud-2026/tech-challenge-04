# Dossiê de contexto

TL;DR: a parte documental está entregue (README de requisitos e cinco guias). Em 2026-09-23 começou a implementação: plano e arquitetura em `02_TRABALHO/PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html`; decisões D-009 e D-010; entrega em 2026-11-17.

Última atualização: 2026-09-24, Claude (Opus 5.5).

## 1. Objetivo
Ler integralmente o enunciado e as aulas; produzir requisitos obrigatórios/bônus com evidência por página e cinco guias HTML autocontidos, no padrão do guia CI/CD da Fase 3, ligados aos requisitos por selos. Nada foi implantado: os guias são material de estudo, não prova de infraestrutura.

## 2. Regras/preferências
Pt-BR, explicação simples antes da técnica, fonte com página em cada afirmação, datas ISO, `[INCERTO]` para dúvidas, preservação dos originais, sem commit/push. Marca d'água com nome e e-mail do titular nunca é transcrita.

## 3. Situação atual
- `docs/requisitos/README.md`: 42 REQ-OBR, 2 REQ-BON, 4 SUG, dúvidas Q-01 a Q-14, coluna "Módulo(s)" preenchida e índice dos guias publicado.
- `docs/requisitos/REQUISITOS.html`: espelho gerado do README, para as âncoras dos selos funcionarem localmente.
- Cinco guias em `docs/aulas-fiap/*/GUIA-ESTUDO-*.html`: Welcome (21 KB), Observabilidade (186 KB), Opensource (74 KB), APM (391 KB) e Automação de incidentes (90 KB).
- Os 32 PDFs originais conferidos por SHA-256: intactos.

## 4. Arquivos/caminhos
Raiz: `C:\Users\Gabriel\Documents\GitHub\tech-challenge-04`. Enunciado na raiz; 31 PDFs de aula em cinco pastas de `docs/aulas-fiap`. Referência somente leitura: `../tech-challenge-03/docs/aulas-fiap/02_CI-CD/GUIA-ESTUDO-CI-CD.html`. Trabalho auxiliar em `00_COLAB_IA/02_TRABALHO`; versões substituídas em `00_COLAB_IA/_ARQUIVO_MORTO`.

## 5. Ferramentas do repositório (todas em `02_TRABALHO`)
| Script | Para que serve |
|---|---|
| `extrair-pdfium-2026-09-16_v01.py` | Extrai o texto integral dos PDFs (o modo layout do pypdf falhava). |
| `preparar-leitura-2026-09-21_v01.py` | Limpa cabeçalhos repetidos e mapeia páginas com código, figura ou tabela. |
| `renderizar-paginas-2026-09-16_v01.py` | Renderiza páginas em PNG para conferência visual do código. |
| `guia_base.py` + `guia-base-2026-09-16_v01.css` | Cabeçalho, CSS, legenda, sumário e seção de conexão comuns a todos os guias. |
| `montar-guia-2026-09-16_v01.py` | Monta um guia a partir de fragmentos HTML + `config.json` + `conexoes.json`. |
| `validar-guias-2026-09-16_v01.py` | Valida estrutura, âncoras, links, IDs, código escapado, mojibake e dados pessoais (modo `--fragmento` para peças isoladas). |
| `gerar-espelho-requisitos-2026-09-20_v01.py` | Regenera `REQUISITOS.html` a partir do README. |
| `mapear-modulos-readme-2026-09-20_v01.py` | Preenche a coluna "Módulo(s)" e o índice do README pela cobertura real dos guias. |

Python com `pypdfium2`: `C:\Users\Gabriel\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` — o do PATH não tem a biblioteca. Use sempre `-X utf8`.

## 6. Decisões
D-001 caminhos; D-002 evidência e status; D-003 metadados de autoria; D-004 fragmentos e validação; D-005 auditar antes de marcar; D-006 espelho HTML dos requisitos; D-007 autoria inline do B4; D-008 coluna de módulos derivada da cobertura.

## 7. Pendências
P-001 concluída. P-002: implementação em oito etapas (E0–E7), ainda não iniciada, com sete perguntas em aberto. Detalhes em PENDENCIAS e no plano v02.

## 8. Glossário
OTel: OpenTelemetry. APM: Application Performance Monitoring. GitOps: estado desejado versionado e reconciliado. Self-Healing: tentativa automática de mitigação. NRDB/NRQL: banco e linguagem de consulta da New Relic. UST: Unified Service Tagging. MELT: métricas, eventos, logs e traces.

## 9. Cuidados
Guia não certifica funcionamento. Opção do enunciado não implica nota extra. Exemplo de aula não é requisito. Conteúdo que não vem da aula nem do enunciado vai em bloco "Complemento" rotulado. Duas execuções com subagentes já foram perdidas por limite de uso: grave cada arquivo assim que ficar pronto.

## 10. Resumo das conversas
2026-09-16: usuário definiu duas fases, cinco guias, checklist e verificação obrigatórios; dúvidas não bloqueantes viram `[INCERTO]` e o trabalho continua. 2026-09-20 e 21: usuário pediu para retomar após os limites de uso serem reiniciados. 2026-09-23: usuário pediu o plano de implementação com diagramas de alto e baixo nível, sem inventar dados; respondeu às decisões de ferramenta, repositório, equipe e prazo (D-009).

## 11. Memória interna ↔ espelho
Contexto compartilhado neste dossiê; histórico da Fase 3 usado apenas como referência editorial. Memória global não foi alterada.

## 12. Instruções iniciais para o próximo assistente
Ler LEIA-PRIMEIRO, PENDENCIAS e o topo do LOG. Retomar pelo item V. Para alterar qualquer guia, edite o fragmento correspondente em `02_TRABALHO/fragmentos/<modulo>/` (APM e Incidentes) ou o script gerador `_v02` (Welcome, Observabilidade e Opensource), remonte e revalide — nunca edite o HTML final à mão. Não comitar nem publicar sem autorização.
