# Dossiê de contexto

TL;DR: a parte documental está entregue (README de requisitos e cinco guias). Em 2026-09-23 foi elaborado o plano de implementação: plano e arquitetura em `02_TRABALHO/PLANO_E_ARQUITETURA_FASE4_2026-09-23_v02.html`; decisões D-009 e D-010; entrega em 2026-11-17.

Última atualização: 2026-10-20, Codex.

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
P-001 concluída. P-002: execução E0–E7 não iniciada. P-003: AWS escolhida em 2026-10-20, conta/cotas/orçamento pendentes; não presumir crédito por criar outra conta. P-004: importação Git com histórico proposta e ainda não executada. Detalhes em PENDENCIAS, auditoria atual e plano v02.

## 8. Glossário
OTel: OpenTelemetry. APM: Application Performance Monitoring. GitOps: estado desejado versionado e reconciliado. Self-Healing: tentativa automática de mitigação. NRDB/NRQL: banco e linguagem de consulta da New Relic. UST: Unified Service Tagging. MELT: métricas, eventos, logs e traces.

## 9. Cuidados
Guia não certifica funcionamento. Opção do enunciado não implica nota extra. Exemplo de aula não é requisito. Conteúdo que não vem da aula nem do enunciado vai em bloco "Complemento" rotulado. Duas execuções com subagentes já foram perdidas por limite de uso: grave cada arquivo assim que ficar pronto.

## 10. Resumo das conversas
2026-09-16: usuário definiu duas fases, cinco guias, checklist e verificação obrigatórios; dúvidas não bloqueantes viram `[INCERTO]` e o trabalho continua. 2026-09-20 e 21: usuário pediu para retomar após os limites de uso serem reiniciados. 2026-09-23: usuário pediu o plano de implementação com diagramas de alto e baixo nível, sem inventar dados; respondeu às decisões de ferramenta, repositório, equipe e prazo (D-009).

## 11. Memória interna ↔ espelho
Contexto compartilhado neste dossiê; histórico da Fase 3 usado apenas como referência editorial. Memória global não foi alterada.

## 12. Instruções iniciais para o próximo assistente
Ler LEIA-PRIMEIRO, PENDENCIAS e o topo do LOG. Retomar P-003 e a etapa E0 de P-002; V já concluída em 2026-09-21. Para alterar qualquer guia, edite o fragmento correspondente em `02_TRABALHO/fragmentos/<modulo>/` (APM e Incidentes) ou o script gerador `_v02` (Welcome, Observabilidade e Opensource), remonte e revalide — nunca edite o HTML final à mão. Não comitar nem publicar sem autorização.

## 13. Snapshot de 2026-10-13

Guias/README novamente validados: 0 erros; 32 fontes intactas por SHA-256. O 04 ainda não contém serviços ou infraestrutura e só tem dois commits de insumos (2026-09-16); entregáveis continuam não rastreados. Código AWS da Fase 3 foi lido para estimar impacto da migração, sem alterações.

Usuário informou que o crédito AWS acabou e pediu recomendação sobre Azure. Azure tem ofertas US$200/30 dias e Students US$100/12 meses, verificadas em fontes oficiais nesta data; elegibilidade/cotas da conta [INCERTO]. AKS Free não elimina custo dos nós. Recomendação registrada: trabalhar E0/E1 local primeiro e comparar orçamento AWS curto com Azure elegível. Azure ainda não aprovada como provedor.

Prazo informado pelo usuário: 2026-11-17; 35 dias desde 2026-10-13. Q-01 segue aberta (AKS permitido p.2; vídeo nomeia EKS p.5). Fontes, impacto em SQS/DynamoDB e limites de QA em `02_TRABALHO/ANALISE_ESTADO_E_OPCOES_CLOUD_2026-10-13_v01.md`.

## 14. Atualização de 2026-10-20

Usuário escolheu continuar AWS e informou intenção de criar outra conta. Conta não foi criada/verificada nesta sessão; a regra oficial atual exclui cliente que já teve conta dos créditos para novos clientes. Fontes e detalhes no plano de importação de 2026-10-20.

Recomendação de importação: merge dos históricos em branch do 04 a partir da base 6100879 da Fase3 (main/dev iguais e checkout limpo), preservando os materiais do 04. Cópia/fork/subtree foram comparados; método segue como proposta (D-013). Nenhum commit/push ou mudança Git foi feito. AWS é decisão confirmada (D-012); E0/P-004 continuam pendentes. Backend e identidades devem corresponder à conta efetivamente usada.
