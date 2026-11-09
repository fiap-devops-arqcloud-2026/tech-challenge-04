# Dossiê de contexto

TL;DR: código e histórico da Fase 3 importados na branch import-fase3 e integrados à dev em 2026-10-20; main intacta. Requisitos, cinco guias e materiais da Fase 4 preservados. README/CI/ArgoCD adaptados; integração e instrumentação locais aprovadas em 2026-10-27. Conta AWS e APM externo pendentes.

Última atualização: 2026-10-28, Codex.

Orientação de contas em 2026-10-28 (P-011): [guia AWS/GitHub/New Relic/PagerDuty/Slack](02_TRABALHO/GUIA_CONTAS_E_ACESSOS_FASE4_2026-10-28_v01.md) concluído. Cadastro, permissões e integrações descritos; nenhuma conta/configuração externa criada ou validada. P-003/E1 externa e demais provas externas continuam pendentes. Confirmar elegibilidade/cobrança AWS e continuidade do plano Free PagerDuty; não solicitar segredos no chat. Primeiro aceite externo recomendado: exportar os traces locais ao New Relic. Guia não altera D-009/D-014/D-016 nem autoriza implantação/publicação/envio de notificações.

## 1. Objetivo
Ler integralmente o enunciado e as aulas; produzir requisitos obrigatórios/bônus com evidência por página e cinco guias HTML autocontidos, no padrão do guia CI/CD da Fase 3, ligados aos requisitos por selos. Código-base importado e validado localmente; nada foi implantado na nova conta. Guias são material de estudo, não prova de infraestrutura.

## 2. Regras/preferências
Pt-BR, explicação simples antes da técnica, fonte com página em cada afirmação, datas ISO, `[INCERTO]` para dúvidas, preservação dos originais; commits e merge locais autorizados para esta importação, sem push/PR/main. Marca d'água com nome e e-mail do titular nunca é transcrita.

## 3. Situação atual
- `README.md` principal: atualizado em 2026-10-27 com as explicações de telemetria/ferramentas/Kubernetes, localização cluster/SaaS, exemplos condicionais de pods Collector e três diagramas da arquitetura planejada e publicação. Instrumentação local aprovada em 2026-10-27; implantação e APM externo continuam pendentes.
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
D-001 caminhos; D-002 evidência e status; D-003 metadados de autoria; D-004 fragmentos e validação; D-005 auditar antes de marcar; D-006 espelho HTML dos requisitos; D-007 autoria inline do B4; D-008 coluna de módulos derivada da cobertura; D-009 ferramentas; D-012 AWS; D-014 importação; D-015 consolidação didática no README; D-016 instrumentação local antes do APM externo.

## 7. Pendências
P-001, P-004 e P-006 concluídas. P-002: E0 parcialmente concluída com a importação; E1–E7 pendentes, e o plano precisa dos refinamentos da conferência de 2026-10-21. P-003: AWS escolhida em 2026-10-20, conta/cotas/orçamento pendentes; não presumir crédito por criar outra conta. P-005/P-008: integração e instrumentação locais aprovadas em 2026-10-27 (19 spans/5 serviços e SQL de auth/flag/targeting), laboratório encerrado; New Relic externo continua pendente. Detalhes em PENDENCIAS, auditoria atual e plano v02.

## 8. Glossário
OTel: OpenTelemetry. APM: Application Performance Monitoring. GitOps: estado desejado versionado e reconciliado. Self-Healing: tentativa automática de mitigação. NRDB/NRQL: banco e linguagem de consulta da New Relic. UST: Unified Service Tagging. MELT: métricas, eventos, logs e traces.

## 9. Cuidados
Guia não certifica funcionamento. Opção do enunciado não implica nota extra. Exemplo de aula não é requisito. Conteúdo que não vem da aula nem do enunciado vai em bloco "Complemento" rotulado. Duas execuções com subagentes já foram perdidas por limite de uso: grave cada arquivo assim que ficar pronto.

## 10. Resumo das conversas
2026-09-16: usuário definiu duas fases, cinco guias, checklist e verificação obrigatórios; dúvidas não bloqueantes viram `[INCERTO]` e o trabalho continua. 2026-09-20 e 21: usuário pediu para retomar após os limites de uso serem reiniciados. 2026-09-23: usuário pediu o plano de implementação com diagramas de alto e baixo nível, sem inventar dados; respondeu às decisões de ferramenta, repositório, equipe e prazo (D-009).

## 11. Memória interna ↔ espelho
Contexto vigente compartilhado neste dossiê. O código/histórico da Fase 3 foi importado, preservando sua origem; a colaboração histórica em `docs/00_COLAB_IA` não substitui esta pasta. Memória global atualizada por pedido explícito do usuário em 2026-10-20: `C:/Users/Gabriel/.codex/memories/extensions/ad_hoc/notes/2026-10-20T18-29-00-tech-challenge-04-importacao.md`, com escopo e limites da validação, sem credenciais ou dados da conta.

## 12. Instruções iniciais para o próximo assistente
Ler LEIA-PRIMEIRO, PENDENCIAS e o topo do LOG. Retomar na dev: P-003 para conta/backend e E1 externa para New Relic; P-005/P-008 locais concluídas, não repetir a implementação. V e importação P-004 já concluídas. Para alterar qualquer guia, edite o fragmento correspondente em `02_TRABALHO/fragmentos/<modulo>/` (APM e Incidentes) ou o script gerador `_v02` (Welcome, Observabilidade e Opensource), remonte e revalide — nunca edite o HTML final à mão. A importação recebeu autorização de commits/merge locais; publicação/push/PR/main continuam aguardando pedido.

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


## 18. Passos locais concluídos — 2026-10-27

Usuário reiterou explicação leiga/técnica do backend e autorizou passos1/2. Relatório Terraform de 2026-10-22 reconferido: 40 .tf, sete módulos locais, oito chamadas, 51 blocos resource, 13 data e três backends S3 parciais. Isso não inventaria AWS ativa; conta/bucket/estado remoto não foram consultados. Não há arquivos reais backend.hcl/tfvars nas três raízes; entradas por ambiente não foram investigadas.

Baseline anterior à instrumentação aprovado em 2026-10-22; regressão final aprovada em 2026-10-27. Go/Python e Collector local implementados. Trace final com 19 spans/5 serviços, quatro CLIENT PostgreSQL (auth2/flag1/targeting1), Redis, produtor/consumidor SQS, DynamoDB e ack. Árvore de pais, resposta de negócio, oito eventos esperados, logs JSON5, sanitização e health aprovados. Correção SQL move RealDictCursor para o pool/connect; o novo teste rejeita a ausência dos spans. 13 testes Go principais + oito subtestes; 20 testes Python também dentro das imagens. SDK/exporters fixados; nenhuma métrica SDK ou coleta de logs pelo Collector foi adicionada nesta etapa.

Arquivos de referência: RELATORIO_TERRAFORM_BACKEND_2026-10-22_v01.md; RELATORIO_PASSO1_REVALIDACAO_2026-10-27_v01.md; RELATORIO_PASSO2_OBSERVABILIDADE_LOCAL_2026-10-27_v01.md; RESULTADO_PASSOS_LOCAIS_2026-10-27_v01.json, todos em 02_TRABALHO. Runbook em observability/README.md. QA bruta em 02_TRABALHO/qa-passos-locais-2026-10-27, ignorada. Backups em _ARQUIVO_MORTO/2026-10-27_retomada-passos-locais e instrumentacao-go/python.

Final: removidos somente os 12 contêineres e dois volumes descartáveis tc04-integration; evidências em bind mount preservadas. 39 materiais04 intactos, 33 exclusões preexistentes preservadas, Fase3 limpa, dev/HEAD/main intactos. Sem commit/push/PR/AWS/CI remoto nem atualização de memória global. Próximo: E1 externa com chave New Relic local (usuário escolheu local primeiro), P-003 conta/backend/cotas/orçamento/identidades, depois etapas de cluster, métricas/logs e incidentes. Não marcar REQ-OBR-11/14/15 ou toda E1 concluídos por esta prova local.

## 19. Revisão integral frente à FIAP — 2026-10-28

P-009 concluída após interrupção de créditos em 2026-10-27. PDF integral lido/renderizado, 42 IDs cruzados com código/IaC/GitOps/CI/documentação e evidências. Relatório vigente desta revisão: `02_TRABALHO/REVISAO_GERAL_FASE4_2026-10-28_v01.md`; matrizJSON e verificação com a mesma data; três pareceres setoriais preservados. Dois requisitos comprovados localmente (02/13), 10 parciais, 28 pendentes e 2 a confirmar. A contagem não mede nota/esforço; há obrigações de implementação e de evidência do mesmo componente. Catálogo normativo antigo permanece intacto; matriz registra execução.

Achados: F-017 targeting indisponível pode virar HTTP 200/result=true/Rule:null no cache (sonda27 em cópia isolada, cinco cenários); F-018 auth transforma erroSQL em 401; F-019 manifests Kubernetes ainda não ativam OTel nem incluem stack; F-020 CI funcional não chama prova integradaOTel; F-021 plano/calendário/runbook e duas âncoras históricas desatualizados; F-022 revisão das exceçõesTrivy vencida, sem conclusão sobre CVEs atuais. Backlog P-010 mantém ações, separando recomendações de exigênciasFIAP. Não houve correção do código nesta revisão.

Validações27 reconferidas28: Terraformfmt/validate nas3raízes aprovados, renderGitOps23objetos, 19 spans/5 serviços e suites13Go+8 subtestes/20 Python. Preservação atual205arquivos do inventário, 28 fontes do ensaio, 39materiaisprotegidos/33 exclusões anteriores; fonte03 limpa e dev/HEAD/main intactos.37 links dos novos pareceres e 42 citações de página conferidos. Aulas31PDFs não relidas integralmente; hashes e cinco guias/validador conferidos. Contas/CIremoto/cluster/APM não consultados; ausência de prova não prova inexistência externa.

Próximo agente: usar LOG+PENDENCIAS+matriz 42; não repetir importação/instrumentação/revisão concluída. Tratar achados antes do cenário de alerta e continuar E 1externa/P-003/E 2–E 7 mediante escopo autorizado. Falta stack/3sinais/APM/alerta/incidente/ChatOps/self-healing, publicação e demonstração real, vídeo≤25 min e PDF com quatroprints/identificação/links/justificativas. Confirmar entrega individual e horário/canal;2026-11-17 é prazo informado pelo usuário, meta interna 2026-11-12. Sem mudança de decisões arquiteturais, memória global, operaçãoAWS, commit/push/PR/main.
