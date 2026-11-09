# Dossiê de contexto

TL;DR: código e histórico da Fase 3 importados na branch import-fase3 e integrados à dev em 2026-10-20; main intacta. Requisitos, cinco guias e materiais da Fase 4 preservados. README/CI/ArgoCD adaptados; conta AWS e integração Docker pendentes.

Última atualização: 2026-10-22, Codex.

## 1. Objetivo
Ler integralmente o enunciado e as aulas; produzir requisitos obrigatórios/bônus com evidência por página e cinco guias HTML autocontidos, no padrão do guia CI/CD da Fase 3, ligados aos requisitos por selos. Código-base importado e validado localmente; nada foi implantado na nova conta. Guias são material de estudo, não prova de infraestrutura.

## 2. Regras/preferências
Pt-BR, explicação simples antes da técnica, fonte com página em cada afirmação, datas ISO, `[INCERTO]` para dúvidas, preservação dos originais; commits e merge locais autorizados para esta importação, sem push/PR/main. Marca d'água com nome e e-mail do titular nunca é transcrita.

## 3. Situação atual
- `README.md` principal: atualizado em 2026-10-22 com as explicações de telemetria/ferramentas/Kubernetes, localização cluster/SaaS, exemplos condicionais de pods Collector e três diagramas da arquitetura planejada e publicação. Instrumentação e implantação continuam pendentes.
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
D-001 caminhos; D-002 evidência e status; D-003 metadados de autoria; D-004 fragmentos e validação; D-005 auditar antes de marcar; D-006 espelho HTML dos requisitos; D-007 autoria inline do B4; D-008 coluna de módulos derivada da cobertura; D-009 ferramentas; D-012 AWS; D-014 importação; D-015 consolidação didática no README.

## 7. Pendências
P-001, P-004 e P-006 concluídas. P-002: E0 parcialmente concluída com a importação; E1–E7 pendentes, e o plano precisa dos refinamentos da conferência de 2026-10-21. P-003: AWS escolhida em 2026-10-20, conta/cotas/orçamento pendentes; não presumir crédito por criar outra conta. P-005: engine Linux do Docker Desktop confirmada em 2026-10-22 (29.6.1, contexto desktop-linux); teste integrado ainda não executado. Detalhes em PENDENCIAS, auditoria atual e plano v02.

## 8. Glossário
OTel: OpenTelemetry. APM: Application Performance Monitoring. GitOps: estado desejado versionado e reconciliado. Self-Healing: tentativa automática de mitigação. NRDB/NRQL: banco e linguagem de consulta da New Relic. UST: Unified Service Tagging. MELT: métricas, eventos, logs e traces.

## 9. Cuidados
Guia não certifica funcionamento. Opção do enunciado não implica nota extra. Exemplo de aula não é requisito. Conteúdo que não vem da aula nem do enunciado vai em bloco "Complemento" rotulado. Duas execuções com subagentes já foram perdidas por limite de uso: grave cada arquivo assim que ficar pronto.

## 10. Resumo das conversas
2026-09-16: usuário definiu duas fases, cinco guias, checklist e verificação obrigatórios; dúvidas não bloqueantes viram `[INCERTO]` e o trabalho continua. 2026-09-20 e 21: usuário pediu para retomar após os limites de uso serem reiniciados. 2026-09-23: usuário pediu o plano de implementação com diagramas de alto e baixo nível, sem inventar dados; respondeu às decisões de ferramenta, repositório, equipe e prazo (D-009).

## 11. Memória interna ↔ espelho
Contexto vigente compartilhado neste dossiê. O código/histórico da Fase 3 foi importado, preservando sua origem; a colaboração histórica em `docs/00_COLAB_IA` não substitui esta pasta. Memória global atualizada por pedido explícito do usuário em 2026-10-20: `C:/Users/Gabriel/.codex/memories/extensions/ad_hoc/notes/2026-10-20T18-29-00-tech-challenge-04-importacao.md`, com escopo e limites da validação, sem credenciais ou dados da conta.

## 12. Instruções iniciais para o próximo assistente
Ler LEIA-PRIMEIRO, PENDENCIAS e o topo do LOG. Retomar na dev: P-003 para conta/backend e P-005 para Docker; depois E1. V e importação P-004 já concluídas. Para alterar qualquer guia, edite o fragmento correspondente em `02_TRABALHO/fragmentos/<modulo>/` (APM e Incidentes) ou o script gerador `_v02` (Welcome, Observabilidade e Opensource), remonte e revalide — nunca edite o HTML final à mão. A importação recebeu autorização de commits/merge locais; publicação/push/PR/main continuam aguardando pedido.

## 13. Snapshot de 2026-10-13

Guias/README novamente validados: 0 erros; 32 fontes intactas por SHA-256. O 04 ainda não contém serviços ou infraestrutura e só tem dois commits de insumos (2026-09-16); entregáveis continuam não rastreados. Código AWS da Fase 3 foi lido para estimar impacto da migração, sem alterações.

Usuário informou que o crédito AWS acabou e pediu recomendação sobre Azure. Azure tem ofertas US$200/30 dias e Students US$100/12 meses, verificadas em fontes oficiais nesta data; elegibilidade/cotas da conta [INCERTO]. AKS Free não elimina custo dos nós. Recomendação registrada: trabalhar E0/E1 local primeiro e comparar orçamento AWS curto com Azure elegível. Azure ainda não aprovada como provedor.

Prazo informado pelo usuário: 2026-11-17; 35 dias desde 2026-10-13. Q-01 segue aberta (AKS permitido p.2; vídeo nomeia EKS p.5). Fontes, impacto em SQS/DynamoDB e limites de QA em `02_TRABALHO/ANALISE_ESTADO_E_OPCOES_CLOUD_2026-10-13_v01.md`.

## 14. Snapshot anterior à autorização/importação — 2026-10-20 (superado pela seção 15)

Usuário escolheu continuar AWS e informou intenção de criar outra conta. Conta não foi criada/verificada nesta sessão; a regra oficial atual exclui cliente que já teve conta dos créditos para novos clientes. Fontes e detalhes no plano de importação de 2026-10-20.

Recomendação de importação: merge dos históricos em branch do 04 a partir da base 6100879 da Fase3 (main/dev iguais e checkout limpo), preservando os materiais do 04. Cópia/fork/subtree foram comparados; método segue como proposta (D-013). Nenhum commit/push ou mudança Git foi feito. AWS é decisão confirmada (D-012); E0/P-004 continuam pendentes. Backend e identidades devem corresponder à conta efetivamente usada.

## 15. Fechamento da importação — 2026-10-20

Branch atual: dev. `import-fase3` aponta para `31f92e4`, já ancestral da dev pelo merge `cb81b00`. Histórico da Fase 3 mantém o commit `6100879`; checkpoint do 04 é `4c76a2d`. Main do 04 continua em `003a707`. Não houve push, PR ou operação de nuvem, e o 03 segue limpo e somente leitura.

39 arquivos preexistentes de docs/enunciado 04 intactos por SHA-256; todos os 933 arquivos do manifesto inicial preservados, com versões anteriores das ferramentas/contexto arquivadas. Serviços correspondem à base 03. Caches, renderizações e extrações locais não foram excluídos nem versionados; fontes dos guias, contexto e entregáveis foram versionados.

README e CLAUDE apontam o estado do 04; CI valida dev sem AWS e exige repository variables antes da publicação futura; ArgoCD/OIDC apontam ao repo 04, mantendo main como destino futuro. Backend parcial, estados próprios da Fase 4 e `expected_aws_account_id` impedem presumir a conta antiga. Conta, bucket, região e outputs reais ainda pendentes.

Validado: Terraform nas três raízes sem backend; 23 objetos Kustomize; YAML/gates de nove workflows e dez casos da trava AWS; builds Go (sem testes unitários); AST Python de seis arquivos; Compose config; guias, requisitos e links. Docker Desktop não iniciou, então a integração em contêineres ficou em P-005. Runtime AWS e CI remoto não executados. Resultado completo em `02_TRABALHO/RESULTADO_IMPORTACAO_FASE3_2026-10-20_v01.md`.

## 16. Documentação consolidada — 2026-10-22

Após as explicações de 2026-10-21 sobre sinais, ferramentas e Kubernetes, o usuário perguntou se o README as reunia. P-006/D-015 consolidaram uma síntese no README principal, com os três diagramas renderizados e revisados, fontes oficiais e links para plano/backlog. O conteúdo expõe o desenho futuro, sem declarar implantação. O plano v02 e `docs/ARQUITETURA.md` histórico não foram alterados.

Validação: 21 links locais, cercas Markdown, três diagramas Mermaid em Chrome headless e inspeção visual; revisão técnica independente sem achados. Os 39 arquivos originais/entregáveis preexistentes do 04 continuam intactos por SHA-256. As 33 exclusões locais anteriores de materiais históricos da Fase 3 não foram alteradas. Sem commit/push/PR/nuvem ou atualização de memória global nesta revisão.

Retomada permanece na dev: P-003, P-005 e E1, além dos refinamentos de P-002. Não usar o exemplo de uma réplica do gateway como escolha já fechada. Capturas locais ignoradas em `02_TRABALHO/qa-readme-2026-10-22/`; resultados em `verificacao-readme-2026-10-22_v01.json` e `resultado-render-readme-2026-10-22_v01.json`. Versões anteriores dos documentos em `_ARQUIVO_MORTO/2026-10-22_readme-observabilidade/`.

## 17. Ordem de avanço confirmada — 2026-10-22

Usuário perguntou os próximos passos. Conferência somente leitura confirmou Docker Linux disponível, removendo o bloqueio anterior de P-005. Próxima ação executável: testar a base Compose; depois E1 com Go/Python, Collector e propagação de contexto. É possível desenvolver/verificar spans localmente sem AWS; exportação e demonstração no New Relic dependem de conta/chave configurada. AWS, PagerDuty e Slack podem ser preparados em paralelo; E2 segue base → imagens publicadas → cluster → k8s, com as autorizações de publicação/implantação ainda pendentes. O calendário antigo continua precisando de atualização para a data informada de 2026-11-17. Nenhum teste, contêiner ou recurso de nuvem foi iniciado nesta orientação.
