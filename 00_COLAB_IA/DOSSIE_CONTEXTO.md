# Dossiê de contexto

TL;DR: B0/B1 e B2 concluídos; preparação do B3 concluída em 2026-11-04 (seção 24): notificações reais validadas, testes e ensaio da falha aprovados, plano da base com 0 destroy e custo oficial de US$ 9,82/dia. Pré-requisitos fechados em 2026-11-05 (seção 25): tokens validados, orçamento criado e créditos em US$ 120. Teste da confiança OIDC no CI (seção 26) e painel dos nós (seção 27). Falta só a autorização dos tópicos 5 e 6.

Última atualização: 2026-11-05, Claude (Opus 5.5).

Atualização 2026-10-28 14:47: usuário informou conclusão do guia IAM/OIDC até passo7. Provedor, policy, role, Variables e consultas IAM são concluídos por relato; nenhuma prova de CI remoto/cluster decorre disso. Prosseguir com inventário, correção F-023 na dev, backend próprio, adoção de recursos manuais e plan revisado. Não recriar role nem reutilizar state antigo. PR/main/apply permanecem fora do pedido de orientação. Registros seguintes sobre ausência da role refletem momentos anteriores.

F-023/P-012 em 2026-10-28: usuário informou que a role IAM ainda não existe e pediu instruções de criação. [Guia e políticas](02_TRABALHO/role-github-oidc-2026-10-28_v01/LEIA-ME.md) preparados. Consulta autenticada somente leitura confirmou repo04 privado e subject OIDC imutável com ownerID287716251/repoID1373159817. Terraform ainda tem trust sem IDs; corrigir antes de aplicar. Guia propõe somente main para publicação e permissões ECR restritas; nenhum recurso AWS ou código foi alterado.

Atualização de conta em 2026-10-28: usuário informou ter criado nova conta AWS e feito login CLI; ECR em preparação pela interface. Não houve validação autenticada da identidade, créditos ou recursos pelo agente. Inventariar criações manuais antes do Terraform e importar se necessário. CI continua consumindo Variables AWS_REGION/ECR_REGISTRY/AWS_ROLE_ARN e autenticação OIDC; login local não configura o GitHub. P-003 permanece aberto para validação/cobrança/cotas/backend.

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
Contexto vigente compartilhado neste dossiê. O código/histórico da Fase 3 foi importado, preservando sua origem; a colaboração histórica em `docs/00_COLAB_IA` foi mesclada e removida do caminho ativo em 2026-11-01, com originais preservados em `_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA` (D-017). Memória global atualizada por pedido explícito do usuário em 2026-10-20: `C:/Users/Gabriel/.codex/memories/extensions/ad_hoc/notes/2026-10-20T18-29-00-tech-challenge-04-importacao.md`, com escopo e limites da validação, sem credenciais ou dados da conta.

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

## 20. Herança da Fase 3, mesclada em 2026-11-01

**Escopo desta seção:** relato histórico extraído pelo Claude, revisto pelo Codex em 2026-11-01. Fontes e medições da Fase 3 não provam recursos da conta atual. Comandos são referências para um runbook futuro, não ordem de execução. As referências de código “conferidas em 2026-11-01” vêm da extração do Claude, exceto retificações explicitadas; não houve nova auditoria dos cinco serviços. Acervo integral: [_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA](_ARQUIVO_MORTO/2026-11-01_mescla-colab-fase3/acervo-integral-docs-00_COLAB_IA/). [Índice dos 158 itens](02_TRABALHO/mescla-colab-fase3-2026-11-01_v01/INDICE_RASTREABILIDADE_2026-11-01_v01.md) (122 destinados a este dossiê; demais distribuídos por protocolo/organização/pendências/histórico).

**Retificação atual:** inventário autenticado AWS/GitHub de 2026-10-28: 34/34 verificações; trust OIDC local: 8/8 testes offline. ECR e provedor não estão apenas “por relato”. O bucket segue confirmado pelo usuário em 2026-10-30, sem nova checagem AWS. Contas SaaS criadas por relato; ingestão, alertas e CI remoto ainda não comprovados. As seções anteriores mantêm snapshots datados.

Esta seção reúne o que a memória de trabalho da Fase 3 (`docs/00_COLAB_IA/`, 39 arquivos) tem de útil para decidir na Fase 4: arquitetura, números, boas práticas, armadilhas e lições de vídeo e relatório. Os caminhos de "Fonte F3" são relativos a `docs/00_COLAB_IA/`. Os originais podem ser recuperados com `git show 3b21e65:docs/00_COLAB_IA/ARQUIVO` e no repositório `tech-challenge-03`. IDs da Fase 3 levam o prefixo F3-. IDs sem prefixo são da Fase 4, e os achados da análise P-015 aparecem como TFB-, TFC-, TFK-, GIT-, CIC-, CMP-, DOC- e XCL-. O ID da conta antiga aparece sempre como `<CONTA_FASE3>`. Nada aqui comprova recurso na conta nova.

### 20.1 O que a Fase 3 entregou (arquitetura e recursos)

- **Arquitetura de referência (2026-09-09).** Monorepo com `services/`, `terraform/`, `gitops/`, `.github/workflows/` e `docs/`, tudo em us-east-2. A VPC tem 2 sub-redes públicas e 2 privadas em AZs distintas, com EKS e bancos nas privadas. Os 5 serviços rodam no EKS. Há 2 RDS PostgreSQL (auth_db, flags_db), targeting_db em StatefulSet, ElastiCache Redis, SQS com DLQ consumida pelo analytics (grava na tabela DynamoDB `ToggleMasterAnalytics`) e 5 ECR com lifecycle e scan on push. Não há Ingress: o acesso é por `kubectl port-forward`. Fonte F3: _ARQUIVO_MORTO/ARQUITETURA.md (l. 11-29, 61-91); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 86-87, 97, 109, 140). Na Fase 4: já descrita em `docs/ARQUITETURA.md` §1-4 (histórico) e no README (l. 27-39, 141-164). Falta arquitetura vigente com OTel/Prometheus/Loki/Grafana/New Relic/PagerDuty/Slack/self-healing (DOC-07, GIT-01). O overlay prod está em sentinelas e a main ainda não tem `gitops/` (GIT-03, TFK-03).
- **Serviços, portas e nomes canônicos (2026-08-27 a 2026-09-15).** auth-service e evaluation-service em Go 1.25. flag-service, targeting-service e analytics-service em Python 3.12. Portas 8001 (auth), 8002 (flag), 8003 (targeting), 8004 (evaluation) e 8005 (analytics). Nomes recuperados da Fase 2: namespace e cluster `togglemaster`, ECR `<servico>-service`, fila `togglemaster-events`, cache `togglemaster-redis`, tabela `ToggleMasterAnalytics`, bancos auth_db/flags_db/targeting_db com usuário `toggle`, tag `v1.0.0-<commit>`. Toda a configuração vem de variáveis de ambiente (DATABASE_URL, REDIS_URL, AWS_REGION, AWS_SQS_URL, AWS_DYNAMODB_TABLE, MASTER_KEY, SERVICE_API_KEY, PORT, `*_SERVICE_URL` e, depois, SQS_ENDPOINT e DYNAMODB_ENDPOINT), e a varredura não achou credencial hardcoded. Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 24, 32, 130); _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 279-281, 411-421). Na Fase 4: continua no código (`docker-compose.yaml`, `gitops/overlays/prod`). Variáveis OTEL_*, nomes de dashboards e labels devem seguir o padrão (F-019, GIT-02, GIT-11).
- **Fluxo e contrato da API (2026-09-15).** O evaluation lê o Redis com cache de 30 s, consulta flag e targeting com a SERVICE_API_KEY e publica na SQS. O analytics consome a fila e grava no DynamoDB. `GET /evaluate` é aberto e exige `flag_name` e `user_id`; outros nomes devolvem 400. `POST :8002/flags` e `POST :8003/rules` exigem Bearer com a chave, criada em `POST :8001/admin/keys` com Bearer MASTER_KEY e mostrada uma única vez (71 caracteres, prefixo `tm_key_`). Só a regra PERCENTAGE existe (100 = sempre true, 0 = sempre false). A regra com user_ids é aceita e ignorada, e o `/health` não consulta o banco. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 310-326, 1231-1266, 1334-1370); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 58-62). Na Fase 4: confirmado em `evaluator.go:24` e `:262-264`, `handlers.go:36-37` e `key.go:11-16`. Para resultado determinístico em tráfego e cenários de erro, usar PERCENTAGE 100/0 levando em conta o TTL e reaproveitar `scripts/integration/test-flow.py` (F-017, F-018, GIT-15).
- **Terraform em três camadas (2026-08-27 a 2026-09-15).**
  - Base (`terraform/`): VPC, IGW, 1 NAT controlado por `enable_nat_gateway`, 5 ECR, SQS + DLQ, DynamoDB, provedor OIDC e role do CI.
  - Cluster (`terraform/cluster/`): EKS e node group, 2 RDS PostgreSQL 16 db.t3.micro, Redis cache.t3.micro e roles IRSA. As senhas dos RDS nascem aqui e vão ao Secrets Manager.
  - k8s (`terraform/k8s/`): namespaces, 5 Secrets, StorageClass gp3, ArgoCD por Helm e a Application.
  - Há 7 módulos próprios (ecr, eks, elasticache, iam-ci, irsa, messaging, rds) e só a VPC vem da comunidade. A ligação entre camadas é por `terraform_remote_state`.
  - Fonte F3: DECISOES.md (l. 21, 136-154, 232-244); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 524-528). Na Fase 4: as chaves de estado passaram de `prod/` para `phase4/prod/`, com backend parcial (`terraform/README.md` l. 7-19). A camada k8s ainda não tem nada de observabilidade (TFK-01).
- **Híbrido Terraform + ArgoCD (2026-07-18).** Os guias de IaC (8 aulas) e de CI/CD (7 aulas) recomendam Terraform para o cluster e os componentes fixos e ArgoCD para as aplicações dinâmicas; Terragrunt é opcional. Fonte F3: LOG_DE_TRABALHO.md (l. 537-539, 549-551). Na Fase 4: serve de critério para decidir se cada peça da stack entra como release Helm/Terraform ou como Application (GIT-01, TFK-01, TFC-05).
- **Ciclo GitOps (2026-08-27 a 2026-09-15).** Kustomize com `base/` por serviço e um único overlay `prod/`. Depois de lint, SAST, SCA e scan, a imagem vai ao ECR com tag `v1.0.0-<sha7>`. O último job roda `kustomize edit set image` e comita no overlay com `[skip ci]`. A Application `togglemaster` (namespace argocd) lê `gitops/overlays/prod` na main, com automated, prune, selfHeal e reconciliação de 30 s, e o CI nunca roda `kubectl apply`. O fluxo foi demonstrado ponta a ponta em 2026-09-15. Fonte F3: DECISOES.md (l. 184-194, 208-230, 256-266); LOG_DE_TRABALHO.md (l. 61-65). Na Fase 4: confirmado em `_ci-go.yml:583` e `:602` e em `terraform/k8s/argocd.tf:191` e `:297-325` (CIC-07, CIC-09, GIT-14, TFK-11).
- **Overlay prod (2026-09-09 a 2026-09-15).** `kustomization.yaml` guarda as 5 imagens, escritas só pelo job. `patches/endpoints.yaml` guarda REDIS_URL e AWS_SQS_URL, e `patches/irsa.yaml` os 2 ARNs IRSA. REDIS_URL e ARNs vêm de `terraform output redis_url` e `irsa_role_arns` depois do apply do cluster. O esquema precisa casar com o TLS: `redis://` sem TLS, `rediss://` com TLS (variável `redis_transit_encryption`). Em 2026-09-09 o placeholder PREENCHER impediu o evaluation de conectar. A mudança vai à main por branch temporária ou PR, e o ArgoCD reconcilia com intervalo configurado de 30 s, sem garantia de conclusão nesse prazo. Tags diferentes entre serviços são esperadas quando apenas alguns mudam; conferir os runs antes de concluir que houve falha. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 817-857); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 72-76); _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 977-1006). Na Fase 4: os campos estão com sentinelas (`*.conta-pendente.invalid`, `CONTA_AWS_PENDENTE`). Ver `gitops/README.md` l. 24-36 (GIT-03, GIT-06, TFC-08).
- **Nove workflows (2026-09-09 a 2026-09-15, conferido em 2026-11-01).** São 5 chamadores, 2 reutilizáveis (`_ci-go.yml`, `_ci-python.yml`), Terraform Check e Compose Integration. Os jobs são build/testes, lint (golangci-lint v2.13.2; flake8/pylint), SAST (gosec v2.29.0; bandit), SCA (Trivy fs), image e gitops. O job image tem `needs: [build, lint, sast, sca]`: é um portão antes da publicação, não uma checagem depois. Fonte F3: _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 194-230, 299-338); _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (l. 47-57). Na Fase 4: confirmado (`_ci-go.yml:326`, `:388`, `:602`). O self-healing não existe (CIC-01), e os jobs herdam permissões amplas (CIC-03).
- **Identidade sem chave AWS estática.** O CI assume `togglemaster-github-actions` por OIDC, e os pods usam IRSA com menor privilégio: o evaluation só publica na fila, e o analytics só consome a fila e grava na tabela. Isso substituiu as chaves que a Fase 2 guardava em Secret. Uma versão antiga do SECURITY.md citava LabRole por engano. MASTER_KEY e SERVICE_API_KEY são segredos estáticos de aplicação, então não se deve afirmar "nenhuma credencial estática". Fonte F3: DECISOES.md (l. 14, 200); _ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md (l. 53, 114-116). Na Fase 4: ver `docs/ARQUITETURA.md` §6. Collector e self-healing devem seguir OIDC/IRSA (TFB-05, XCL-08). A situação da trust está em 20.4.
- **Segredos gerados pelo Terraform (2026-09-01 a 2026-09-15).** Não há External Secrets Operator. O Terraform gera as senhas com `random_password`, as dos RDS também vão ao Secrets Manager, e a camada k8s aplica os 5 Secrets. O contrato fica em `gitops/SECRETS-CONTRATO.md`. Perdas aceitas: Secret fora do GitOps, rotação não sincronizada e valores em texto no tfstate. Fonte F3: DECISOES.md (l. 118-136). Na Fase 4: é o padrão candidato para as chaves de New Relic, PagerDuty e Slack e o token do self-healing, mas o contrato não as cobre (XCL-09, TFK-04, TFC-09).
- **Bancos: 2 RDS e targeting em StatefulSet (2026-08-27).** A conta da Fase 3 recusou a terceira instância RDS ("maximum number of instances available with free plan accounts", F3-F-023). O desvio foi combinado com o professor, mas o comprovante escrito não foi localizado. O StatefulSet exige o addon `aws-ebs-csi-driver` e a StorageClass default; sem eles, o PVC fica Pending. Fonte F3: DECISOES.md (l. 170-182); LOG_DE_TRABALHO.md (l. 389). Na Fase 4: confirmar o limite na conta nova (P-003) e, se o desvio continuar, declará-lo (ver 20.5). Ver também GIT-09 (imagem do Postgres com tag móvel).
- **Node group e sizing (2026-08-27).** O plano gratuito recusou t3.medium ("not eligible for Free Tier"). Ficou 2 x c7i-flex.large (2 vCPU / 4 GB), com mínimo 1, desejado 2 e máximo 4. Foram descartados t3.micro (~4 pods por nó), t4g (ARM, imagens x86) e m7i-flex.large (mais caro). Fonte F3: DECISOES.md (l. 156-168). Na Fase 4: a conta não inclui Collector, Prometheus, Loki, Grafana nem agente New Relic. A elegibilidade na conta nova não foi verificada (TFC-01, TFC-04, XCL-10, F-026, P-003).
- **Estado esperado do cluster (2026-09-15).** São 2 nós Ready. No namespace togglemaster: 5 Deployments com 1 réplica, StatefulSet `postgres-targeting` (mínimo 6 pods 1/1 Running), 5 Secrets e StorageClass gp3. A Application fica Synced/Healthy e há 2 HPAs (evaluation, analytics). `aws-ebs-csi-driver` e `metrics-server` nascem no Terraform do cluster. A UI do ArgoCD abre por `port-forward svc/argocd-server 8080:80`, com a senha no Secret `argocd-initial-admin-secret`. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 907-915, 1374-1412). Na Fase 4: Prometheus e Loki com persistência também dependem da StorageClass default (`terraform/modules/eks/main.tf:306-319`; TFK-09).
- **Ambiente local e teste integrado (2026-09-04 a 2026-09-15).**
  - O Compose sobe 9 contêineres: 5 serviços, postgres-auth, postgres-app, Redis e DynamoDB Local (sem healthcheck).
  - Usa as portas 8000-8005, 5433, 5434 e 6379; só 8001-8005 são ajustáveis pelo `.env`.
  - O Compose Integration roda `scripts/test-compose.sh` com Moto e limite de 20 min. Cobre health, credencial inválida, chave, persistência, flags 0%/100%, cache com TTL e SQS → DynamoDB. Confirmou 7 eventos persistidos e revelou uma regressão real de merge.
  - Não cobre RDS gerenciado, IAM/IRSA, EKS, ECR, rede nem ArgoCD.
  - Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 85-256, 345-415); _ARQUIVO_MORTO/TESTE_COMPOSE.md (l. 1-44).
  - Na Fase 4: o projeto se chama `tc04-integration`, mas o guia histórico ainda limpa `tc03-integration` (CMP-04, CMP-07, CMP-08, CIC-15, F-020).
- **Versões e imagens base (2026-09-11, conferido em 2026-11-01).** Go 1.25 (exigido por golang.org/x/crypto v0.55.0), golangci-lint 2.x, alpine:3.20 nos serviços Go, python:3.12-slim nos Python, EKS 1.34, db.t3.micro e cache.t3.micro. Fonte F3: _ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md (l. 184-209). Na Fase 4: os valores estão iguais no código. Reconferir antes do primeiro build (CIC-08, TFC-03, F-022).
- **Criptografia e lacunas (2026-09-09).** RDS, ElastiCache, DynamoDB, ECR, EBS e o bucket de estado tinham criptografia em repouso. RDS e Redis só aceitavam tráfego do security group do cluster. Ficaram de fora o scan de IaC, o Prowler, o CloudTrail e os logs do plano de controle do EKS, e o Redis segue sem TLS em trânsito. Fonte F3: _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (l. 100, 110-116); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 165, 171). Na Fase 4: ver `docs/ARQUITETURA.md` l. 352-372 (CIC-06, TFC-07, TFC-08, TFC-11).
- **Requisitos da Fase 3 que não podem regredir.** Terraform modular com estado remoto no S3. CI por serviço com build, testes, lint, SAST, SCA, bloqueio de CRITICAL e push no ECR com tag de hash. GitOps com ArgoCD e sync automático. A exceção 2 RDS + pod foi aceita por relato na Fase 3, sem comprovante escrito localizado. Fonte F3: _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-fiap-texto-por-pagina-2026-09-09.txt (l. 53-118). Na Fase 4: base de REQ-OBR-25 (EKS e ArgoCD rodando com a nova stack); GIT-04 e TFK-06.

### 20.2 Números medidos (tempos, custos, tamanhos)

Todos os números são da conta da Fase 3. A Fase 4 terá mais recursos e precisa medir de novo.

| Medida | Valor | Data | Fonte F3 |
|---|---|---|---|
| Apply da base só ligando o NAT | 2m24s | 2026-09-11 | _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 1594-1612) |
| Apply do cluster | 15m42s | 2026-09-11 | idem |
| Apply da camada k8s (duas etapas) | 4m44s | 2026-09-11 | idem |
| Sessão do NAT ligado ao fim do destroy | 3h17m | 2026-09-11 | idem |
| Destroy da k8s | 13 recursos em 1m04s (EBS de 5 GB apagado pelo driver) | 2026-09-15 | LOG_DE_TRABALHO.md (l. 67-70) |
| Destroy do cluster | 35 recursos; RDS ~2 min, EKS ~3 min, ElastiCache 4m17s | 2026-09-15 | idem |
| Destroy da base | 35 recursos em 1m40s (OIDC reaproveitado) | 2026-09-15 | idem |
| Primeiro apply da base | 19 de 33 criados; 7 falharam por sobras da Fase 2; o apply seguinte criou os 14 restantes | 2026-09-07 | _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 391-401) |
| Base aplicada | 33 recursos, NAT desligado, state de 61 KiB | 2026-09-07 | LOG_DE_TRABALHO.md (l. 51, 54) |
| Plan da base do zero | 35 (OIDC false) ou 36 (OIDC true); a diferença para 33 não é explicada [INCERTO] | 2026-09-15 | _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 585-592) |
| Plan do cluster | 35 recursos | 2026-09-10 | LOG_DE_TRABALHO.md (l. 153) |
| Plan -destroy | 14 (k8s), 35 (cluster), 36 (base), todos com exit 0 | 2026-09-11 | _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 5-15) |
| Camada k8s criada com github_token vazio | 13 recursos | 2026-09-15 | LOG_DE_TRABALHO.md (l. 223) |
| Overlay prod renderizado | 23 objetos | 2026-09-09 a 2026-09-15 | _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (l. 83) |
| Requests dos 5 Deployments | 450m CPU / 512Mi; postgres-targeting soma 100m / 128Mi | 2026-08-27 (conferido em 2026-11-01) | _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 432) |
| Estimativa de recursos com ESO (cortado depois) | ~1,25 vCPU e 1,9 GiB | 2026-08-27 | idem (l. 428-432) |
| Merge → commit do robô (flag-service) | ~2 min | 2026-09-15 | _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 289-291) |
| PR #6 | 7 workflows success, 5 imagens `v1.0.0-7ab0602`, 5 commits chore(gitops) | 2026-09-10 | LOG_DE_TRABALHO.md (l. 215-219) |
| dev atrás da main | 19 commits | 2026-09-08 | DECISOES.md (l. 61-77) |
| main após o PR #3 | 12 commits: 4 humanos e 8 do bot | 2026-09-09 | _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 123-130) |
| Bucket de estado após destroy total | 687 bytes; frações de centavo no Cost Explorer | 2026-09-11 | LOG_DE_TRABALHO.md (l. 200) |
| Gravação sem áudio | 17min58s, mais de 1 GB, todas as amostras zeradas | 2026-09-11 | _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 3-5, 137-142) |
| Links conferidos no fechamento | 81 links, 0 quebrados | 2026-09-11 | LOG_DE_TRABALHO.md (l. 146) |
| Revisão adversarial dos rascunhos | 54 problemas | 2026-09-11 a 2026-09-15 | LOG_DE_TRABALHO.md (l. 42, 117) |
| Placar de requisitos | 24 comprovados, 6 escritos sem apply, 9 não iniciados (vídeo e relatório) | 2026-09-09 | _ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md (l. 74-85) |

**Custos (AWS Pricing Calculator, us-east-2, 730 h, tudo ligado, 2026-09-11).** Fonte F3: _ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md (l. 1-35).

| Item | US$/mês |
|---|---|
| EKS 1.34, suporte padrão | 73,00 |
| EC2 2 x c7i-flex.large, 20 GB por nó | 126,99 |
| RDS 2 x db.t3.micro Single-AZ, 20 GB gp3 | 30,88 |
| ElastiCache 1 x cache.t3.micro | 12,41 |
| VPC (1 NAT, 1 IPv4 público, 1 GB processado) | 36,54 |
| EBS gp3 5 GB | 0,40 |
| Secrets Manager, 2 segredos | 0,81 |
| **Total** | **281,03** (US$ 3.372,36 em 12 meses; ~US$ 0,385/h) |

- Uma sessão de 2 h custava ~US$ 0,77 e uma de 3 h ~US$ 1,15. A estimativa deixa de fora S3, ECR, SQS, DynamoDB e transferência.
- Ressalva: outras fontes citam US$ 0,37/h para a camada cluster. Uma conta anterior, menos completa, dava US$ 0,368/h (~US$ 269/mês), e a diferença não é explicada. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 1567-1581); DECISOES.md (l. 144).
- Na estimativa histórica, o NAT sozinho custava US$ 0,045/h (~US$ 33/mês). Com IPv4 público, a estimativa citava US$ 0,050/h. Uma semana esquecida custa ~US$ 7,50 a 8 sem nada rodando, e um fim de semana com tudo ligado passa de US$ 18. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 51-56, 1583-1587, 1611-1612). Na Fase 4: `terraform/variables.tf:102` cita só ~US$ 33/mês (TFB-10).
- A fonte histórica atribuía ao plano de controle do EKS US$ 0,10/h em suporte padrão e US$ 0,60/h em suporte estendido (6x). O dado vem da página de preços consultada em 2026-09-09. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 101-103).
- Valores citados sem fonte de preço (2026-08-27 a 2026-09-11):
  - ALB/Ingress: ~US$ 16-20/mês.
  - Nó c7i-flex.large: ~US$ 0,085/h, cerca do dobro da t3.medium.
  - Sair do plano gratuito economizaria ~US$ 48/mês em EC2, mas exigiria método de pagamento.
  - O saldo de crédito da conta antiga não foi transportado para esta memória vigente e não prova saldo na conta nova.
  - Fonte F3: DECISOES.md (l. 144, 164, 176, 210, 216). Na Fase 4: TFC-06, F-026.

**Estimativas (não medidas).**
- Base do zero: reservar 10 min.
- Republicar imagens: 2 a 4 min, em paralelo ao cluster.
- Schemas e seed: ~15 min por sessão.
- Recriar tudo do zero: 40 min a 1 h, mais as imagens.
- Apply do cluster: 15-30 min.
- Pipeline: ~3 min na dev e ~5 min completo na main.
- Application Synced/Healthy: 1-2 min após a k8s.
- HPA com `<unknown>`: ~2 min.
- O plano de gravação de 2026-09-15 previa ~2h20, com plano C se o ambiente não subisse até ~T+90.
- Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 588-592, 747-749); _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 154-181, 1057-1059).

### 20.3 Boas práticas que continuam valendo

- **Ordem das camadas.** Subida: base → publicação das 5 imagens no ECR → cluster → `aws eks update-kubeconfig` → k8s em duas etapas → schemas e seed. Destruição: k8s → cluster → base. A base vem primeiro também porque cria o OIDC e a role que destravam o CI. Fonte F3: DECISOES.md (l. 29-43); _ARQUIVO_MORTO/GUIA_EXECUCAO.md (l. 35-38). Na Fase 4: `terraform/README.md:15`; P-015 B3 prevê apply da base → merge na main → cluster → k8s (DOC-02, F-021).
- **Plano salvo.** Usar `terraform plan -out=<nome>.tfplan`, conferir o resumo e aplicar o arquivo, nunca o apply interativo: num bloco colado, a linha seguinte vira a resposta do yes. Na subida, "to destroy" deve ser 0. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 64, 69, 194-217). Na Fase 4: `expected_aws_account_id` é obrigatório, então um plan sem tfvars pede valor (`terraform/README.md:25`).
- **Um terraform.tfvars local por camada, fora do Git.** Apply e destroy devem ler os mesmos `enable_nat_gateway`, `create_github_oidc_provider`, `github_repository` e `gitops_repo_url`. Um `-var` esquecido no destroy pode apagar um provedor OIDC de outro dono, e o tfvars da base não é lido pelas subpastas. Fonte F3: DECISOES.md (l. 16, 20, 39, 41). Na Fase 4: os tfvars locais ainda faltam (P-003, TFK-10).
- **Pré-voo sem custo (2026-09-10/15).**
  - Ambiente: `aws sts get-caller-identity` (a conta deve ser a dona do bucket e do ECR), Terraform 1.11 ou mais novo, kubectl, aws, `gh auth status`, AWS_PROFILE e `AWS_PAGER=""`.
  - OIDC: `aws iam list-open-id-connect-providers`.
  - Base: `terraform output github_actions_role_arn`. "No outputs found" com código 0 indica base inexistente.
  - Token do repositório: testar com `git ls-remote`, o mesmo mecanismo do ArgoCD. Token fine-grained de organização pode ficar pendente ou nascer com o dono errado.
  - Antes do cluster: versão do EKS em suporte padrão, tipo de nó nas AZs, cota de EIP, número de RDS, chart do ArgoCD publicado, nenhum NAT vivo e `init.sql` presentes.
  - Fonte F3: LOG_DE_TRABALHO.md (l. 221-234); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 446-520); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (l. 43-157).
  - Na Fase 4: testar também as chaves de New Relic, PagerDuty e Slack (P-003, TFK-02, TFK-11).
- **Sessões curtas e encerramento planejado.** Fazer antes tudo o que não custa, concentrar o cluster em poucas sessões de até 3 h (ensaio e gravação), prever o encerramento de cada sessão. A política atual de manter base/NAT ou destruir tudo ainda depende da posse dos recursos e da autorização de execução. Anotar a hora em que o NAT liga. Fonte F3: _ARQUIVO_MORTO/GUIA_EXECUCAO.md (l. 39-42); _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 104-145). Na Fase 4: P-015 B3-B5 (proposta: stack em 2026-11-05–2026-11-06, gravação até 2026-11-10, encerramento após prova); recalcular com a stack.
- **Tags de custo.** `project=fiap` e `phase=<fase>` em minúsculas, uma vez por `default_tags`. A chave de tag diferencia maiúsculas e gera grupos separados no Cost Explorer. O bucket de estado recebe as tags à mão. Fonte F3: DECISOES.md (l. 246-254). Na Fase 4: `phase = "4"` (`terraform/variables.tf:58`); as tags do bucket novo não foram conferidas (TFB-07).
- **Trivy bloqueante com exceções nominais.** Só CRITICAL bloqueia: os 4 scans usam `severity CRITICAL`, `exit-code 1` e `ignore-unfixed false`. O `.trivyignore` tem exceções com data, motivo e revisão. Em 2026-09-09 havia 3 CVEs de perl-base em python:3.12-slim (revisão em 2026-10-15), e alpine:3.20 tinha zero CRITICAL. Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 30, 87); _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 910-943). Na Fase 4: a revisão está vencida (CIC-08, F-022, CIC-10).
- **Sem `continue-on-error` em scans; medir antes de endurecer.** Com `continue-on-error`, o CVE-2026-56854 (CRITICAL, golang.org/x/crypto v0.20.0) passava com o pipeline verde. Pipeline verde não prova código seguro. Antes de mudar um gate, rodar a ferramenta no artefato real. Fonte F3: _ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md (l. 176-190); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 232-235). Na Fase 4: não há `continue-on-error` em 2026-11-01. Revisar todo job novo, inclusive o de self-healing.
- **Laço idempotente para gravar no repositório.** Com concurrency compartilhada, só 1 execução rodava e 1 ficava pendente, e as anteriores eram canceladas. O `git pull --rebase` conflitava no `kustomization.yaml`. A solução foi um laço de até 5 tentativas (fetch, `reset --hard origin/main`, edit, commit, push, espera crescente) que termina com "A tag ja esta correta". Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 283-292). Na Fase 4: `_ci-go.yml:569-614`. Se adotado, o self-healing que gravar no Git deve considerar concorrência/idempotência; reset --hard só em checkout descartável de CI, nunca na árvore local. Referência (CIC-01, CIC-07).
- **Versões que existem, fixadas por SHA.**
  - `trivy-action@0.28.0` nunca existiu e foi trocada pelo SHA da v0.36.0.
  - gosec v2.21.4 não compilava e passou a v2.29.0.
  - golangci-lint v1.61 recusava `go.mod` novo; hoje roda a action v9 com a ferramenta v2.13.2.
  - `kubectl kustomize` não tem `edit`, por isso o job instala o kustomize 5.4.3 (F3-F-027, F3-P-036).
  - Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 238-239, 381-389, 425).
  - Na Fase 4: só o Trivy está por SHA (CIC-04, CIC-11).
- **Verificações locais mínimas.** `terraform fmt -check`/`validate` nas 3 camadas, `kubectl kustomize gitops/overlays/prod` (23 objetos), YAML dos workflows e Trivy contra a imagem real. O `scripts/validate-all.sh` roda inteiro no Git Bash do Windows desde 2026-09-09. Antes de fechar um documento: links e âncoras, `bash -n`, parser de PowerShell sem executar, `git diff --check` e o PDF conferido. Fonte F3: LOG_DE_TRABALHO.md (l. 252, 269, 303, 320, 146, 163, 204). Na Fase 4: nenhum workflow chama o `validate-all.sh`, e os manifests GitOps não são validados no CI (CIC-05, CIC-09, GIT-14, DOC-10).
- **Legenda de evidência.** No checklist de infraestrutura da Fase 3, `[x]` exigia prova AWS/CI. Na Fase 4, marcar cada tarefa conforme seu próprio aceite: uma tarefa local concluída não depende de AWS; um requisito externo depende de prova externa. `[~]` vale para escrito e validado sem apply, ou parcial consciente. `[ ]` é não iniciado. A revalidação de 2026-09-09 sugeriu separar escrito, validado, executado e evidenciado. Fonte F3: _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (l. 9-18); _ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md (l. 73). Na Fase 4: a matriz da §19 já usa comprovado/parcial/pendente/a confirmar, e o catálogo ainda mostra tudo como Pendente (DOC-09).
- **Critério literal de requisito.** O enunciado virou checklist: 39 obrigatórios (F3-O-01 a F3-O-39), 9 opcionais (F3-R-01 a F3-R-09) e 9 sugestões das aulas (F3-S-01 a F3-S-09). Obrigatório era o que estava em "Requisitos Técnicos" e "Entregáveis". Antes de cortar algo, varria-se o PDF por palavras-chave: em 2026-08-27, os termos de Ingress apareceram zero vezes. Fonte F3: LOG_DE_TRABALHO.md (l. 405-407, 465-467); _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 412-420). Na Fase 4: o critério já está em LEIA-PRIMEIRO, D-002 e `docs/requisitos/README.md:46`. Busca por palavra é apoio; ausência da palavra não substitui leitura integral do enunciado.
- **Combinado com professor ou tutor fica por escrito.** O comprovante do desvio de 2 RDS não foi localizado até 2026-09-15. Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 32). Na Fase 4: vale para Q-03 (entrega individual, REQ-OBR-41), Q-05, Q-06 e Q-13 (DOC-08).
- **Básico funcionando antes de extras.** Extras que valeu manter na Fase 3: OIDC/IRSA, DLQ, estados separados, Kustomize, workflows reutilizáveis e Compose integrado. Não afirmar que um extra vale ou não vale nota. Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 69); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 159-175). Na Fase 4: a regra "sem peça nova em runtime" não se aplica literalmente, porque o enunciado exige Collector, Prometheus, Loki, Grafana e APM.
- **Classificação de controles (estudos de 2026-07-18).**
  - Gates essenciais: Gitleaks, SAST, SCA, scan de imagem e de IaC. DAST é muito útil; DefectDojo e dashboards são diferenciais.
  - Controles essenciais: MFA, OIDC, menor privilégio, rede restrita, criptografia, segredos e auditoria. Prowler é muito útil, Falco é diferencial e CASB fica fora do núcleo.
  - Fonte F3: LOG_DE_TRABALHO.md (l. 501-503, 525-527).
  - Na Fase 4: não há varredura de segredos nem scan de IaC no CI (CIC-05, CIC-06).
- **Documentação alinhada ao código.** Em 2026-09-09, um documento mandava criar chaves AWS estáticas no GitHub (o oposto do OIDC) e outros citavam Ingress, 3 RDS, LabRole ou o ESO. A correção reduziu cada texto antigo a um índice (F3-P-049). O relatório e o README eram montados a partir desses documentos. Fonte F3: LOG_DE_TRABALHO.md (l. 254-263, 262, 419); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 78-95). Na Fase 4: `docs/ARQUITETURA.md` e `docs/GUIA_DE_REPRODUCAO.md` são históricos e já divergem do código (gatilhos do CI, `phase=3`, `tc03`, testes Python). A seção OTel do relatório depende de arquitetura vigente (DOC-02, DOC-06, DOC-07, CIC-16).
- **Sincronização histórica da dev.** O roteiro da Fase 3 sugeria `git switch dev`, `git fetch origin` e `git merge --ff-only origin/main`. Não executar esse bloco automaticamente; conferir divergência e alterações locais e agir dentro da autorização vigente. Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 53-64). Na Fase 4: a estratégia deve ser reavaliada quando o CI publicar na main; hoje a main do 04 está em `003a707`, sem `gitops/`.

### 20.4 Armadilhas e lições de operação

**Terraform e backend**
- **Remote state e ordem.** Se a base não foi aplicada, o plan do cluster falha por não achar o estado, e isso é o comportamento correto (2026-08-27). Fonte F3: LOG_DE_TRABALHO.md (l. 257, 345, 351). Na Fase 4: `base_state_key` aponta para `phase4/prod/base.tfstate` (TFC-12).
- **Camada k8s em dois applies (F3-F-043, 2026-09-11).** Em cluster novo, o plan falha com `no matches for kind "Application"`, porque o CRD só existe depois do Helm, e `depends_on` não resolve. A etapa A é `-target=helm_release.argocd`; a etapa B aplica o resto, e o aviso sobre `-target` é esperado. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 774-803); _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 42-48). Na Fase 4: vale para ServiceMonitor, PrometheusRule e operadores. O comentário em `argocd.tf:350-351` contradiz o de `:241` (TFK-01, TFK-05).
- **Bucket de estado.**
  - É a única exceção ao IaC: criado à mão uma vez por conta e apagado por último.
  - Na Fase 3 tinha versionamento, SSE-S3; menção a Bucket Key na fonte é incorreta (Bucket Key pertence ao SSE-KMS), os 4 bloqueios públicos, policy DenyInsecureTransport e lifecycle de 30 dias. O lock é `use_lockfile`; o projeto exige Terraform >=1.11, enquanto o recurso existe desde 1.10.
  - O conteúdo do tfstate pode conter senhas. O backend guarda o objeto remotamente, com criptografia em repouso; arquivos locais excepcionais de recuperação e planos também devem ser protegidos e nunca versionados.
  - Com versionamento, `aws s3 rb --force` não remove versões. Use "Empty" e depois "Delete" no console, sem Terraform ativo.
  - Fonte F3: _ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md (l. 103, 133-291); _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 195-206).
  - Na Fase 4: backend parcial com `backend.hcl` ignorado; bucket criado e confirmado pelo usuário em 2026-10-30 (P-003, TFC-09, TFK-04, DOC-13).
- **Erros comuns de bootstrap (2026-08-27).**
  - `BucketAlreadyOwnedByYou`: o bucket já existe.
  - "same name already exists": o nome está em uso em outra conta.
  - `IllegalLocationConstraintException`: faltou `LocationConstraint=us-east-2`.
  - A região de um bucket existente não muda; planejar outro bucket e eventual migração revisada. Não apagar o bucket atual como correção automática.
  - "Error acquiring the state lock": use `force-unlock` só com certeza.
  - Erro de argumento `use_lockfile`: conferir a versão executada e o backend; o recurso existe desde Terraform 1.10.0.
  - "region ... does not match": o backend aponta para outra região.
  - Fonte F3: _ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md (l. 328-339). Na Fase 4: com o bucket já criado, pesam mais os erros de lock e região. O tema não está nos documentos vigentes.
- **ID da conta no nome do bucket.** O padrão era `togglemaster-tfstate-<CONTA_FASE3>-us-east-2-an`, versionado no `backend.tf`. A mitigação foi manter o repositório privado. Fonte F3: LOG_DE_TRABALHO.md (l. 423). Na Fase 4: o `backend.tf` não tem bucket, mas `docs/GUIA_DE_REPRODUCAO.md:177` e um comentário em `scripts/security-check.sh:11` ainda trazem o ID antigo (DOC-12, XCL-14).
- **Exclusão destrutiva por desenho.** RDS usa `skip_final_snapshot=true` e `deletion_protection=false`, Secrets Manager usa `recovery_window_in_days=0`, ECR usa `force_delete=true` e DynamoDB não tem proteção. O PVC usa reclaim Delete. Cada destroy perde bancos, mensagens, analytics e imagens, e o tfstate não é backup. Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 11-34). Na Fase 4: exportar as evidências antes de destruir (TFC-05).
- **Provedor OIDC já existente (2026-09-14).** O plan não avisa, e o apply falha com `EntityAlreadyExists`, porque só existe um provedor por URL. Com `create_github_oidc_provider=false`, o data source lê o provedor; isso não transfere automaticamente para fora do estado um recurso anteriormente gerenciado. Conferir plano e propriedade antes de mudar a variável. Com false numa conta sem provedor, o plan falha. Fonte F3: DECISOES.md (l. 45-59); LOG_DE_TRABALHO.md (l. 87, 93). Na Fase 4: o provedor foi criado à mão, mas o default e o `tfvars.example:83` continuam true (TFB-03, XCL-03).
- **Apply pode falhar parcialmente.** Normalmente o estado registra recursos concluídos, mas é preciso conferir saída, persistência do state e recursos reais antes de repetir; não presumir integridade automática. `terraform import` é a alternativa não destrutiva. Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 391-401). Na Fase 4: recursos manuais que o Terraform passará a gerenciar exigem import; os apenas reutilizados podem ficar como data sources (TFB-01, TFB-02, XCL-03).
- **Plan como guarda.** Qualquer destroy/replace inesperado no primeiro plan exige parar e investigar backend, estado e configuração; não é diagnóstico automático de estado errado. Um cluster novo deve mostrar "N to add, 0 to change, 0 to destroy". Os registros que atribuem "35 to add" ora à base, ora ao cluster são compatíveis, porque as duas camadas tinham 35. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 751-754, 1491-1494). Na Fase 4: as contagens vão mudar com os imports e a stack.
- **Providers.** Em 2026-08-27 o init resolveu VPC 5.21.0 com AWS 6.62.0. A Fase 3 registrou que "~> 6.0" conflitaria com o módulo [INCERTO: 6.62.0 satisfaz "~> 6.0", e a P-015 recomenda pôr teto]. O `.terraform.lock.hcl` é versionado, e o CI usa Terraform 1.16.0. Fonte F3: LOG_DE_TRABALHO.md (l. 393-401). Na Fase 4: TFB-11, XCL-15.
- **Disciplina de destroy (2026-09-11).** Executar bloco a bloco, sem `-auto-approve`, revisando o plan -destroy. Usar STS, contexto do kubectl fixo e os mesmos tfvars e lockfiles, sem `init -upgrade`. Erro de backend, estado vazio inesperado, workspace diferente ou AccessDenied são motivo para parar. Plan é previsão, não prova. Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 38-75, 216-220). Na Fase 4: `allowed_account_ids` recusa outra conta, mas não substitui o STS.

**EKS, rede e Kubernetes**
- **NAT é o passo mais esquecido (F3-D-017).** O NAT fica na base, que não é destruída nas pausas. Sem NAT nem endpoints/rotas substitutos, os nós privados podem perder acesso a registries e serviços externos. Não é correto afirmar que NAT é sempre necessário ao control plane: depende do endpoint privado/público e da rede. Fonte F3: _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (l. 179-201, 613-627). Na Fase 4: `terraform.tfvars.example:41` traz `enable_nat_gateway = false`, contra o default true (TFK-10, TFC-12).
- **ECR vazio.** A conta nova começa sem imagens, e o destroy da base apaga o ECR. Aplicar a k8s sem imagens gera ImagePullBackOff, com retry de até 5 min; apagar o pod destrava. Só o push na main publica, porque dev, PR e `workflow_dispatch` apenas verificam. Em 2026-09-15 a republicação foi por `gh run rerun`, que usa o workflow e o `.trivyignore` do commit antigo e só vale para runs recentes (~30 dias [INCERTO]). Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 618-736). Na Fase 4: publicar por commit na main que toque `services/<svc>/**` ou `_ci-*.yml`, com base e role já existentes (CIC-13, GIT-03).
- **kubeconfig e principal único.** Depois de recriar o EKS, rodar `aws eks update-kubeconfig`. Só o principal que criou o cluster recebe admin (`bootstrap_cluster_creator_admin_permissions = true`); outro recebe Unauthorized. Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 125-126). Na Fase 4: não há access entry para a role do self-healing (TFC-02, XCL-08).
- **EBS órfão.** O PVC do targeting usa EBS gp3 de 5 GiB, fora dos estados Terraform. O driver só apaga o disco se EKS, nós e CSI estiverem vivos. Conferir com `kubectl wait --for=delete pv/...` (300 s) e `aws ec2 describe-volumes` vazio. Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 77-131). Na Fase 4: a futura stack ainda não define quais PVCs existirão nem quem os removerá; o roteiro deve comprovar essa remoção antes de destruir o cluster (TFC-05).
- **Ordem de encerramento (F3-P-053).** Encerrar a Application (sem finalizer, com selfHeal) → destroy da k8s → confirmar PV/EBS apagado → destroy do cluster → destroy da base → conferir sobras → bucket por último. Antes do destroy da base, procurar o OIDC na lista e parar se ele for compartilhado. Desabilitar os 5 workflows de serviço e aguardar ou cancelar as publicações. Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 7-8); _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 23, 36). Na Fase 4: P-015 B5; a identidade do self-healing ainda será definida; não presumir reutilização da role de imagens.
- **Sobras após o destroy (2026-09-11/15).**
  - Saídas que devem vir vazias: eks, rds, elasticache, NAT available, addresses, volumes, load balancers, log groups, Secrets Manager e get-resources por tags.
  - APIs regionais não cobrem o IAM. Na Fase 3 foram varridas us-east-1, us-east-2, sa-east-1 e o Cost Explorer.
  - Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 167-193).
  - Na Fase 4: `docs/GUIA_DE_REPRODUCAO.md:655` filtra `phase=3`, mas o código usa `phase=4`.
- **O que segue cobrando.** Com a base mantida e o NAT desligado, o custo histórico esperado era baixo, mas ECR/S3, solicitações e outros recursos podem continuar cobrando; conferir faturamento e armazenamento, e um IPv4 solto cobra. Com tudo destruído, sobra só o bucket. Ressalva: o guia de destruição dizia que preservar a base "pode manter custos". Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 1614-1620); _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 212).
- **DependencyViolation em VPC ou subnet.** Identificar ENIs e Load Balancers remanescentes e seus donos, depois retomar o destroy. Nunca apagar state ou lock. Fonte F3: _ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md (l. 165). Na Fase 4: expor o Grafana por Service LoadBalancer reintroduz o risco.
- **Log groups.** Em 2026-09-15 foram limpos log groups de RDS da Fase 2 sem expiração, a VPC da Fase 1 e roles da Fase 2. Fonte F3: LOG_DE_TRABALHO.md (l. 161). Na Fase 4: definir retenção em todo log group, inclusive os da stack (TFC-07). Relevância baixa.
- **Limites da conta anterior.** As recusas de RDS e de t3.medium não provam os limites da conta nova, e outra conta do mesmo cliente não renova a elegibilidade. Fonte F3: _ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md (l. 152-165). Na Fase 4: comentários do código citam "F-023" da Fase 3, que colide com o F-023 atual (XCL-04, TFK-08, F-026).
- **Fim do suporte padrão do EKS 1.34.** A auditoria de 2026-09-09 achou o default 1.31, já fora do suporte padrão desde 2025-11-26, e o default passou a 1.34. A Fase 3 registrou o fim do suporte da 1.34 em 2026-12-01; a P-015 registra 2026-12-02. A entrega (2026-11-17) fica antes. O chart argo-cd 7.7.11 constava dos registros de 2026-09-11. Fonte F3: LOG_DE_TRABALHO.md (l. 155, 224-230, 295-318). Na Fase 4: reconferir com `aws eks describe-cluster-versions`. Não há `upgrade_policy`, e o chart 7.7.11 instala Argo CD v2.13.2, afetado pela CVE-2025-55190 (TFC-03, TFK-02).

**Bancos, seed e diagnóstico**
- **Schemas não aplicados na AWS.** Os `init.sql` de auth e flag só rodam no Compose. Na AWS, aplicar com pod descartável `postgres:16-alpine` e `psql` dentro do cluster, lendo a DATABASE_URL do Secret, e conferir com `\dt`. Sem isso, auth e flag dão `/health` 200 e falham no primeiro INSERT (`relation "api_keys" does not exist`). Lista de pods não vazia também não prova nada; o critério é todos Running e READY 1/1. Fonte F3: _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (l. 331-345, 432-445); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 911-915, 1001-1153). Na Fase 4: não há Job de schema. Alertas e probes não devem depender só do `/health`, e o cenário serve para incidente (GIT-15, F-018, F-021).
- **Seed e dono único da SERVICE_API_KEY.**
  - Passos: port-forward 8001-8004, ler a MASTER_KEY, `POST /admin/keys`, substituir a chave no `evaluation-service-secret` (`kubectl create secret ... --dry-run=client -o yaml | kubectl apply -f -`), `rollout restart`, criar flag e regra PERCENTAGE 100 e conferir com `scan --select COUNT`.
  - O `ignore_changes = [data]` (F3-F-046) evita que um novo apply restaure a chave provisória. A regra é ter um único dono para a chave válida.
  - `/evaluate` 502 com 401 no log indica chave que não confere com o banco. No Compose, isso acontece com chave de outra máquina ou depois de `down -v`, e é preciso recriar o evaluation com `--force-recreate`.
  - Fonte F3: _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (l. 465-557); _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 205-209, 1205-1412).
  - Na Fase 4: o self-healing que reinicia pods não pode restaurar a chave provisória (XCL-09).
- **Tabela de diagnóstico.**
  - ImagePullBackOff com a imagem no ECR: a tag chegou depois do pod; apagar o pod.
  - ImagePullBackOff geral: NAT desligado ou tag ainda placeholder.
  - CreateContainerConfigError: Secret ausente ou com nome divergente.
  - PVC Pending: StorageClass não chamada gp3.
  - "password authentication failed" só no targeting: recriar juntos os 2 Secrets de `random_password.targeting_db`.
  - ArgoCD Unknown com "authentication required": repositório privado sem `TF_VAR_github_token`.
  - QueueDeletedRecently: esperar 60 s.
  - evaluation em CrashLoopBackOff: REDIS_URL ou esquema divergente.
  - Túneis caem quando o pod é trocado: refazer o port-forward.
  - Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 1528-1555); _ARQUIVO_MORTO/RUNBOOK-SESSAO.md (l. 653-664).
  - Na Fase 4: ver `docs/GUIA_DE_REPRODUCAO.md` §11. Vários sintomas servem de cenário controlado de alerta (TFK-11, GIT-03).

**ArgoCD e GitOps**
- **selfHeal, HPA e self-healing.** Em 2026-09-15, o selfHeal reverteu um `kubectl scale` manual. Apagar um pod não demonstra o selfHeal, porque quem recria o pod é o ReplicaSet (observação da extração, não da fonte). Os Deployments com HPA têm `replicas: 1` e a Application não tem `ignoreDifferences`, então ArgoCD e HPA disputam `spec.replicas`. Fonte F3: LOG_DE_TRABALHO.md (l. 61-65); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 477-488, 842-857). Na Fase 4: o self-healing via GitHub Actions deve agir pelo Git ou contar com essa reversão (GIT-04, TFK-06, CIC-01, XCL-08).

**CI/CD**
- **Gatilhos.** Os pipelines rodam com mudanças em `services/<svc>/**`, no workflow do serviço ou no `_ci-*.yml` da linguagem. `gitops/**` fica fora dos filtros, e o `[skip ci]` impede laço. No push na main, image e gitops tentam OIDC e falham se a role não existir. Regra da Fase 3: só levar `services/**` ou `.github/workflows/**` à main depois que a role existir. Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 72-89). Na Fase 4: Terraform Check e Compose Integration agora também rodam em push na dev, e `docs/ARQUITETURA.md:242-243` está desatualizado (CIC-12).
- **`.pylintrc` e `.trivyignore` fora dos filtros.** Mudar só esses arquivos não dispara os workflows. Se a main exigir checks obrigatórios, workflows pulados podem deixar o check pendente. Fonte F3: _ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md (l. 115, 130). Na Fase 4: CIC-14, CIC-02.
- **Robô comita na main.** O job gitops faz `git push origin HEAD:main`, então a main anda sozinha. Exigir PR na main ou criar um ruleset que barre o `github-actions[bot]` faz o job falhar após 5 tentativas. Na Fase 3 a proteção de branch não estava disponível (HTTP 403 com o repositório privado), e dev → PR → main era acordo, não trava técnica. Fonte F3: DECISOES.md (l. 61-77); _ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md (l. 11, 85). Na Fase 4: não presumir proteção remota no repo 04. Merge errado ou force-push volta as tags ao placeholder, e o selfHeal aplicaria (CIC-07).
- **Run cancelado e fila parada.** Um novo push fora da main cancela o run anterior, que aparece como "cancelled" e não como falha: usar `gh run rerun` e `gh run watch`. Com fila em queued por mais de 5 min, cancelar os runs da dev. O plano gratuito permitia 20 jobs simultâneos (2026-09-15), e um merge pela dev gera 3 ondas de runs. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 378-379, 945-952, 1017-1026).
- **Falha de OIDC no CI.** "Could not assume role with OIDC" depois de ~1 min indica role inexistente, `AWS_ROLE_ARN` de outra conta ou `github_repository` diferente. Na Fase 3, a trust aceitava `repo:<owner>/<repo>:*` (StringLike com curinga) e só o `if` do workflow restringia à main. Fonte F3: _ARQUIVO_MORTO/OPERACAO_2026-09-15.md (l. 642-646, 705-706). Na Fase 4: o HEAD 3b21e65 ainda tem StringLike. A árvore de trabalho, sem commit, já usa StringEquals com subject imutável e `ref:refs/heads/<branch>` (conferido em 2026-11-01). O `SECURITY.md:21-22` ainda descreve a trust antiga (F-023, TFB-04, CMP-03).
- **Rerun não resolve CVE novo.** O `gh run rerun` usa o `.trivyignore` do commit original. Para uma CVE crítica nova, investigar aplicabilidade/correção antes de considerar uma exceção (data, motivo, revisão) e publique por commit na main, o que gera tags novas e 5 commits do robô. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 910-943).
- **Trivy local diverge do CI (2026-09-15).** O Trivy 0.74 local não leu pacotes listados depois de `setuptools<81` e `Werkzeug<3`, e o CI (v0.70.0) leu. Na demonstração, `PyYAML==5.3.1` na primeira linha falha com CVE-2020-14343 e `PyYAML==6.0.1` passa. Inserir no topo (`sed -i '1i ...'`). Fonte F3: INSTRUCOES_ASSISTENTES.md (l. 131); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 243-251). Na Fase 4: serve para uma eventual nova demo de SCA (F-022).
- **Upgrade de segurança arrasta o Go.** Subir golang.org/x/crypto para v0.55.0 elevou a diretiva go de 1.21 para 1.25.0. Isso quebrou o Dockerfile (`golang:1.22-alpine`), o go-version do SAST (1.23) e o golangci-lint v1.61. Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 294-301). Na Fase 4: revisar todos os pontos juntos ao adicionar o SDK OTel (D-016, CIC-11).
- **Riscos da primeira execução (2026-09-09).** Em ordem de probabilidade:
  - Trivy fs nos pins antigos de Python (Flask==2.2.2, requests==2.28.1, gunicorn==20.1.0, Werkzeug<3).
  - pylint abaixo de `--fail-under=7.0`.
  - Achados de gosec ou bandit, a corrigir sem afrouxar.
  - CVE de sistema na imagem base.
  - Rodar primeiro na dev. Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 167-188). Na Fase 4: os pins seguem em flag e targeting, e o pylint sem dependências reprovaria o código OTel (CIC-02, CIC-08).
- **`security-check.sh`.** Em 2026-09-09 ele tratava o ID da conta vigente como legado e reprovava toda execução. Foi corrigido para bloquear o ID da Fase 2. Fonte F3: LOG_DE_TRABALHO.md (l. 251, 301). Na Fase 4: em 2026-11-01 ele ainda só bloqueia o ID da Fase 2, não `<CONTA_FASE3>`. Ajustar sem gerar falso positivo com a conta nova (XCL-14, CIC-16).

**Git e ambiente local**
- **Merge escolhendo um lado inteiro.** Em 2026-09-09, um `-X theirs` apagou o suporte a SQS_ENDPOINT/DYNAMODB_ENDPOINT, e só o Compose Integration vermelho revelou o erro. Conferir os trechos exclusivos dos arquivos em conflito e criar tag de backup antes. Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 266-281). Na Fase 4: a dev tem trabalho não comitado e está à frente de origin/dev (XCL-01, CIC-07).
- **Shell no Windows.** Os comandos do runbook rodavam só no Git Bash. O PowerShell 5.1 não suporta `&&`; `--%` é uma alternativa para problemas de passagem de argumentos, não uma exigência universal de -out. Testar o comando no shell indicado. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 15, 77-96). Na Fase 4: DOC-02.

### 20.5 Vídeo, relatório e avaliação da FIAP: o que aprendemos

- **Os entregáveis mudaram.** Na Fase 3 (p. 5-6), o vídeo tinha até 20 min e 5 cenas: IaC, pipeline falhando no passo de segurança e depois passando, tag atualizada no GitOps, ArgoCD sincronizando sozinho e UI com os 5 serviços. O relatório (PDF ou txt) pedia participantes, links, desafios/decisões e print da estimativa de custo. Na Fase 4, o vídeo vai até 25 min e o relatório é só PDF. Ele pede identificação, links, 4 prints (Grafana, trace no APM, ChatOps, self-healing) e justificativa técnica (OTel; Datadog x New Relic; OpsGenie x PagerDuty). Fonte F3: _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 34-58); _ARQUIVO_MORTO/auditoria-2026-09-09/pdf/enunciado-fiap-texto-por-pagina-2026-09-09.txt (l. 142-146). Na Fase 4: REQ-OBR-24 a 42 em `docs/requisitos/README.md:73-91`. Print de custo, link da documentação e desafios não constam da p. 6.
- **Vídeo e relatório ficaram para o fim.** Em 2026-09-09, os 9 itens não iniciados eram vídeo e relatório, com entrega em 2026-09-15. Fonte F3: _ARQUIVO_MORTO/INSTRUCOES_ASSISTENTES_2026-09-14.md (l. 74-85). Na Fase 4: começar já o esqueleto do relatório e o roteiro (DOC-01; P-015 B5 para o vídeo em 2026-11-10–2026-11-12 e B6 para o relatório em 2026-11-13–2026-11-16).
- **Matriz requisito → tela.** A tabela "o que pedem → o que aparece → onde está (custo)" tinha checklist por evidência. Exemplos de cena: job de segurança vermelho com image/gitops cinza, commit do robô com diff do `kustomization.yaml`, card OutOfSync → Synced sozinho. A falha demonstrada tinha causa real (CVE, não lint), e os desvios eram mostrados de frente. Fonte F3: _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 63-74, 964-979); _ARQUIVO_MORTO/EVIDENCIAS.md (l. 12-31). Na Fase 4: montar a matriz para REQ-OBR-25 a 31 e os 4 prints (SUG-01, P-002 E6).
- **Cenas sem cluster primeiro (F3-F-028).** Na Fase 3, metade do vídeo rodava só no GitHub Actions, sem custo AWS. Foram 35-45 min de gravação para 8-9 min finais, feitos antes da sessão paga. Fonte F3: _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 13-31, 78-81); LOG_DE_TRABALHO.md (l. 265, 375). Na Fase 4: a parte sem cluster é menor, porque REQ-OBR-25 exige o EKS com a stack. Candidatas a gravar antes: abertura, configuração das contas e workflows. [INCERTO] se um Service Map gerado do Compose atende REQ-OBR-27 (P-015 B1).
- **Gravar fora de ordem, sem cortar a prova.** As cenas eram gravadas conforme o ambiente ficava pronto, e as esperas eram cortadas. O intervalo entre o commit do robô e o Synced nunca era cortado. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 634-635, 836-837). Na Fase 4: o trecho equivalente é falha → Firing → incidente no PagerDuty → Slack → self-healing (REQ-OBR-28 a 31, CIC-01).
- **Roteiro modelo (2026-09-15, ~18:30 de 20 min).**

  | Cena | Duração | Regra |
  |---|---|---|
  | Abertura | 1:00 | encurtar |
  | IaC | 3:00 | não cortar |
  | DevSecOps | 4:00 | não cortar |
  | Resultado na AWS | 1:30 | encurtar |
  | ArgoCD | 1:30 | não cortar |
  | merge → Synced | 4:00 | nunca cortar |
  | Prova funcional | 2:00 | cortar primeiro |
  | Desafios e custo | 1:30 | cortar |

  Nomes, links e custo iam no relatório. Fonte F3: _ARQUIVO_MORTO/ROTEIRO_VIDEO.md (l. 1-19); _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 828-850). Na Fase 4: dividir os 25 min marcando as cenas de REQ-OBR-25 a 31. Os slides da Fase 3 estão em `docs/apresentacao/ToggleMaster_Fase3.pptx`.
- **Risco na demonstração.** A Fase 3 evitou peça nova em runtime no caminho crítico (motivo do corte do ESO) e passo manual na demo (o robô comita direto, sem fila de PRs). O acesso era por port-forward. Fonte F3: DECISOES.md (l. 69, 124, 212-214). Na Fase 4: aplicar o critério à cadeia alerta → PagerDuty → Slack → self-healing. Resolver antes GIT-04/TFK-06, TFK-11, CIC-07, XCL-08 e TFC-01.
- **Ensaio com folga.** O ensaio (F3-M4) ficou 4 dias antes da gravação (F3-M5), com duas sessões de 3 h previstas. Fonte F3: _ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md (l. 136-148). Na Fase 4: o ensaio da cadeia precisa caber antes do fim do trial do PagerDuty (~2026-11-11). Em 2026-10-30, "Events" aparecia como "Not included" no plano Free (DOC-04, P-015 B4).
- **Narração.** Explicar o porquê de cada evidência:
  - "Se não está no código, não existe".
  - Só o job de segurança fica vermelho.
  - O `[skip ci]` evita laço.
  - "O portão não foi afrouxado, o problema foi resolvido".
  - O tfstate guarda senhas e base64 não é criptografia.
  - Fonte F3: _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 100-109, 212-219, 316-319, 807-810).
  - Na Fase 4: incluir como o Collector roteia os dados (REQ-OBR-26(d)).
- **Áudio.** A gravação de 2026-09-11 saiu muda, e o vídeo foi regravado no dia da entrega. O teste das 08:38 também estava mudo e ninguém o escutou. Suspeitas: a Ferramenta de Captura ficou quase 4 h com o mesmo fluxo de microfone aberto, ou a haste do headset estava levantada. Protocolo, 2 min antes de cada bloco:
  - Conferir a entrada em Configurações > Sistema > Som.
  - Reabrir a ferramenta e fechar Câmera, Teams e Discord.
  - Gravar 15 s e ouvir com fone.
  - Gravar em blocos curtos.
  - Plano B: tela muda com narração depois (Clipchamp ou Gravador de Som).
  - Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 135-150, 856-860); LOG_DE_TRABALHO.md (l. 79).
- **Tela e segredos.**
  - Preparação: abas na ordem de uso, Git Bash maximizado, fonte grande, última linha do plan na tela por 3 s, notificações silenciadas, carregador e rede estável.
  - Comandos que exibem segredo rodam antes de gravar.
  - Fonte F3: _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 83-96, 141).
  - Na Fase 4: vale para a license key do New Relic, a routing key do PagerDuty, o webhook do Slack e tokens do GitHub; `terraform/k8s/outputs.tf:36` mostra o comando da senha do ArgoCD (TFK-04, TFK-09).
- **Formato de runbook que funcionou.**
  - Blocos coláveis com o comando demorado por último, comentário por linha e "Esperado" com a saída exata.
  - Marcas de cena, janelas de terminal, cronograma T+N e contingências prontas.
  - Apêndice com cada comando explicado: o guia passou de 570 para 959 linhas.
  - Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 7-39, 854-1065); LOG_DE_TRABALHO.md (l. 75, 187-190).
  - Na Fase 4: não há roteiro vigente (DOC-02, F-021).
- **Nada é destruído antes de o vídeo estar validado.** Exportar, ouvir o arquivo inteiro com fone, concluir o upload e dar play numa aba anônima. Fonte F3: _ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md (l. 51-52, 739-747). Na Fase 4: P-015 B5.
- **Estrutura do relatório.** O relatório seguiu o da Fase 2, aprovado com nota máxima. Seções: capa institucional, identificação, links, tabela antes/depois, IaC, CI/DevSecOps, CD/GitOps, desafios (desafio + decisão + alternativas), custos, opcionais e anexo. A versão de 2026-09-11 tinha 8 desafios; a final (`docs/RELATORIO_DE_ENTREGA.md`, 2026-09-15) tem 5. Fonte F3: _ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md (l. 7-12, 316-325); LOG_DE_TRABALHO.md (l. 194-200). Na Fase 4: preservar o da Fase 3 e criar documento novo com checklist REQ-OBR-32 a 40 (DOC-01, DOC-07, DOC-11).
- **Desvios a declarar.** Itens:
  - 2 RDS + pod em vez de 3 RDS.
  - Sem Ingress (port-forward).
  - ESO cortado.
  - c7i-flex.large em vez de t3.medium.
  - EKS 1.34 em vez de 1.31.
  - 3 CVEs de perl-base no `.trivyignore`.

  Todos seguem no código. Fonte F3: _ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md (l. 31, 85, 150-152, 307-308); _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 919-961). Na Fase 4: o enunciado não pede seção de desafios. Recomenda-se citar os desvios na justificativa técnica (REQ-OBR-25, REQ-OBR-39/40, TFC-03, CIC-08).
- **Print de custo.** Na Fase 3, o F3-O-39 usou a estimativa de 2026-09-11 e indicava o Cost Explorer filtrado por `project=fiap`. Fonte F3: _ARQUIVO_MORTO/GUIA_GRAVACAO.md (l. 984-990). Na Fase 4: não é requisito; as tags `project=fiap` e `phase=4` já existem. Relevância baixa.
- **Checklist antes do envio (2026-09-14/15).**
  - Sem placeholder de vídeo nem seção opcional vazia, e nada afirmado sem evidência.
  - Manter o marcador `PREENCHER_URL_DO_VIDEO` até a publicação e testar a URL sem login.
  - Regerar e conferir o PDF, e marcar PRELIMINAR enquanto houver pendência.
  - Garantir o acesso do avaliador: o repositório ficou público só em 2026-09-15.
  - Um link para PDF em `output/`, pasta ignorada, ficou quebrado no GitHub.
  - Fonte F3: LOG_DE_TRABALHO.md (l. 97-109); _ARQUIVO_MORTO/build-report-fase3_2026-09-14.py (l. 7-9, 225-366).
  - Na Fase 4: o repo 04 é privado e a entrega individual não tem confirmação registrada (P-015 B6, DOC-05, DOC-08, Q-03, Q-13).
- **PDF reproduzível.** O gerador v00 convertia o Markdown versionado com markdown + WeasyPrint (capa, `@page`, `base_url`). O gerador ReportLab de 2026-09-14 dependia de Segoe UI e trocava travessões por hífen. Fonte F3: _ARQUIVO_MORTO/gerar-relatorio-pdf_2026-09-11_v00.py (l. 1-210); _ARQUIVO_MORTO/build-report-fase3_2026-09-14.py (l. 46-62). Na Fase 4: os geradores podem ser recuperados por `git show` (P-015 B6).
- **Captura automatizada da estimativa.** `capturar-estimativa-aws_2026-09-11.cjs` usa Playwright com Chrome local, viewport 1680x1300, pt-BR, zoom 80% e espera de até 120 s. O script aceitava cookies não essenciais quando não achava a recusa; corrigir isso antes de reaproveitar. Fonte F3: _ARQUIVO_MORTO/capturar-estimativa-aws_2026-09-11.cjs (l. 1-49). Na Fase 4: só se o custo entrar no relatório (XCL-10).

### 20.6 Onde aprofundar

| Tema | Documento atual no 04 | Original da Fase 3 (`git show 3b21e65:docs/00_COLAB_IA/...`) |
|---|---|---|
| Arquitetura, recursos, Secrets, criptografia | `docs/ARQUITETURA.md` (histórico); README l. 27-39 e 141-164 | `_ARQUIVO_MORTO/ARQUITETURA.md`; `DECISOES.md` |
| Camadas, backend e parâmetros pendentes | `terraform/README.md`; `docs/GUIA_DE_REPRODUCAO.md` §3 | `_ARQUIVO_MORTO/BOOTSTRAP-BACKEND-S3_2026-08-27.md` |
| Subida, seed, diagnóstico | `docs/GUIA_DE_REPRODUCAO.md` §5-9 e §11 (histórico) | `_ARQUIVO_MORTO/OPERACAO_2026-09-15.md`; `_ARQUIVO_MORTO/RUNBOOK-SESSAO.md` |
| Destruição e sobras | `docs/GUIA_DE_REPRODUCAO.md` §10; `terraform/README.md:65` | `_ARQUIVO_MORTO/DESTRUIR_AWS_2026-09-11.md` |
| Overlay e valores por conta | `gitops/README.md` l. 24-36; `gitops/SECRETS-CONTRATO.md` | `_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md` (l. 463-547) |
| CI/CD e DevSecOps | `docs/ARQUITETURA.md` §5; README l. 206-218; `.trivyignore` | `_ARQUIVO_MORTO/PENDENCIAS_E_PROXIMOS_PASSOS_2026-09-11.md`; `INSTRUCOES_ASSISTENTES.md` |
| Custos | `docs/RELATORIO_DE_ENTREGA.md` §7; `docs/evidencias/estimativa-custos-aws-2026-09-11.png` | `_ARQUIVO_MORTO/ESTIMATIVA_CUSTOS_AWS.md` |
| Requisitos e critério | `docs/requisitos/README.md`; LEIA-PRIMEIRO; D-002 | `_ARQUIVO_MORTO/CHECKLIST_REQUISITOS_FASE3_2026-09-09.md`; `_ARQUIVO_MORTO/AUDITORIA_FIAP_2026-09-09_v01.md`; `_ARQUIVO_MORTO/REVALIDACAO_AUDITORIA_FIAP_2026-09-09_v01.md` |
| Vídeo e gravação | nada vigente (DOC-02) | `_ARQUIVO_MORTO/GUIA_GRAVACAO.md`; `_ARQUIVO_MORTO/PLANO_GRAVACAO_2026-09-15.md`; `_ARQUIVO_MORTO/ROTEIRO_VIDEO.md` |
| Relatório | `docs/RELATORIO_DE_ENTREGA.md` (Fase 3); relatório da Fase 4 inexistente (DOC-01) | `_ARQUIVO_MORTO/RELATORIO_ENTREGA_FIAP_FASE3_GRUPO203_2026-09-11_v00_PRELIMINAR.md`; `_ARQUIVO_MORTO/gerar-relatorio-pdf_2026-09-11_v00.py`; `_ARQUIVO_MORTO/build-report-fase3_2026-09-14.py` |
| Histórico de decisões e sessões | `00_COLAB_IA/DECISOES.md`, LOG e PENDENCIAS (vigentes) | `DECISOES.md`; `LOG_DE_TRABALHO.md`; `PENDENCIAS_E_PROXIMOS_PASSOS.md`; `_ARQUIVO_MORTO/DOSSIE_CONTEXTO_2026-09-11.md` |
| Achados da Fase 4 citados | `00_COLAB_IA/02_TRABALHO/ANALISE_COMPLETA_FASE4_2026-10-31_v01.md` (P-015); `02_TRABALHO/REVISAO_GERAL_FASE4_2026-10-28_v01.md` (P-009) | — |

Limitações desta mescla: os números são da conta da Fase 3 e não foram remedidos. As referências de código foram conferidas por extração até 2026-11-01, e parte delas depende da árvore de trabalho não comitada (trust OIDC, `security-check.sh`, `tfvars.example`). Preços citados sem fonte não foram verificados.
### 20.7 Retificações e limites da retomada Codex — 2026-11-01

- Fontes primárias das correções de Terraform/S3/ArgoCD: [relatório da mescla](02_TRABALHO/MESCLA_COLAB_FASE3_2026-11-01_v01.md). A restrição >=1.11 no código permanece; só a justificativa histórica estava incorreta. Correções funcionais ficam pendentes.
- Diagnósticos da seção 20.4 são hipóteses históricas: ImagePullBackOff também pode ser IAM, DNS, egress ou imagem ausente; PVC Pending também pode ser provisionador, zona e capacidade. Consultar eventos e estado antes de apagar pods, Secrets ou volumes. Não tratar a tabela como receita destrutiva.
- URL de banco em argumento de psql/kubectl pode aparecer em processos/especificação de pod, mesmo sem eco no terminal; revisar transporte de segredos no novo runbook. Não mostrar sequer prefixos de chaves.
- Campos da API e resultados dos cinco serviços foram relatados nas fontes anteriores; não houve revisão nova desses códigos nesta retomada. CVEs antigos citados nas narrativas não foram todos rechecados.
- P-015 analisa 44 itens = 42 obrigatórios + 2 opções; P-014 tem matriz de 42 obrigatórios. As categorias de status e os escopos diferem; não comparar totais como nota ou regressão.
- D-018 resolve o conflito da documentação pública: referências a assistentes e IDs internos só no diário. Aplicação pública ainda em P-017/B6. As 34 ausências anteriores e decisões de publicação, custos e implantação continuam separadas.
- O guia SaaS já entregue pelo Claude continua orientação. A consolidação não criou chaves, enviou eventos, confirmou plano da conta nem validou integrações externas.

## 21. Contas SaaS e handoff — 2026-11-03

O usuário relatou ter concluído o guia PASSO2 até o 4.3:
- New Relic (US) com license key de ingestão;
- PagerDuty com serviço, política Default e integração Events API v2;
- Slack com canal e Incoming Webhook;
- app do PagerDuty instalado e conectado ao canal.

Faltam o 4.4 (cartão do incidente no canal até Resolved) e o checklist.

O trial do PagerDuty vai de 2026-10-28 a 2026-11-11 (visto na conta pelo usuário; plano "PD Reliability Platform Trial"). A cadeia de incidente deve ser gravada até 2026-11-10.

Os segredos e o Account ID foram informados no chat do Claude. A pedido do usuário, não estão em nenhum arquivo nem no Git. No B1/B4, vão para o `.env` local (ignorado) só com autorização ou pelas mãos do usuário. Recomendado rotacioná-los após a entrega.

O lint Python foi medido em 2026-11-01: o CI atual dá 5,92/5,75/5,50 e, com as dependências, 9,30/9,27/8,61. A próxima ação e as decisões D1–D5 estão no topo de PENDENCIAS.

Atualização 14:30 do mesmo dia (substitui a frase "nenhuma ação" da versão anterior desta seção):
- B0 e B1 concluídos e publicados na dev; o New Relic foi conferido pelo usuário.
- O 4.4 não notificou em nenhum canal; o diagnóstico está em PENDENCIAS.
- D-019 fixa o desenho do B2.
- Commits do B2: `OTEL_*` nos manifestos, ignoreDifferences do HPA, `imports.tf` e 2 × m7i-flex.large.
- A falha proposital do flag-service está sem commit, aguardando o TODO(human) do usuário.
- Nenhuma ação na AWS.

## 22. Retomada OAuth e Events API — 2026-11-03, Codex

Atualização de leitura em 2026-11-03 15:58: Git avançou para 7d50472 após 1c2b0b9, com identidade/permissões e workflow de self-healing. Alterações Terraform k8s ainda locais observadas. Esta consulta não revisou nem validou esse código; ler o estado presente antes de retomar B2. Orientação OAuth/Events V2 reutilizada, ainda sem identificação do cliente OAuth pelo usuário.

Fonte de verdade temporal: atualização posterior da entrada Claude 14:50 no LOG, commit 366bdaa e checkpoint vigente de PENDENCIAS. O 4.4 foi cumprido: trigger/resolve aceitos, e-mail confirmado e cartão Slack observado até Resolved. As frases anteriores de diagnóstico refletem o estado antes dessa conferência. O Codex leu esses registros, sem repetir a consulta externa.

B0/B1 concluídos e New Relic conferido pelo usuário. B2 permanece parcial conforme D-019. Preservados app.py e tests/test_fault.py do flag-service, com TODO(human) reservado ao usuário. D1 autoriza commits curados/push dev; D5 autoriza segredos locais já salvos. PR/main e apply/destroy continuam separados e dependem de aprovação específica no B3.

Pedido atual: explicar ID/segredo OAuth e adição de Events API V2 no serviço existente. [Guia](02_TRABALHO/PAGERDUTY_OAUTH_EVENTS_API_2026-11-03_v01.md) diferencia credenciais e registra fontes oficiais consultadas em 2026-11-03. OAuth é para o aplicativo/assistente; PAGERDUTY_INTEGRATION_KEY é para eventos. [INCERTO] cliente solicitante, callback, tipo e escopos: pergunta assíncrona enviada ao usuário, sem solicitar valores.

Próximos passos: usuário adicionar integração genérica no serviço ToggleMaster Fase 4, atualizar a chave local, validar novo incidente até Resolved e guardar prints. Manter PRTG até validar. Webhook direto do Slack é caminho distinto e continua sem teste confirmado, aguardando autorização registrada pelo Claude. Em seguida retomar restante técnico de B2. Nenhum segredo lido, incidente/mensagem enviado, configuração SaaS, commit/push ou operação AWS nesta orientação.

## 23. B2 técnico — 2026-11-03, Claude

Desenho D-019 implementado e validado localmente, sem AWS:
- **Telemetria:** os 5 serviços mandam OTLP ao `otel-gateway`. O gateway sanitiza os traces e os envia ao New Relic, gera métricas dos spans para o Prometheus (receptor OTLP nativo) e encaminha ao Loki os logs coletados pelo agente DaemonSet.
- **Alerta:** a regra `FlagService5xxAlto` é a proporção de spans SERVER com erro no flag-service, acima de 10% por 1 min. Ela abre incidente no PagerDuty, manda a mensagem detalhada ao Slack e dispara o `repository_dispatch` para o `self-healing.yml`.
- **Self-healing:** o workflow tem lista de serviços permitidos, intervalo mínimo de 600 s, kubectl 1.34.13 e uma role cuja única permissão AWS é `eks:DescribeCluster`. O RBAC só permite `patch` nos 5 Deployments.
- **Fatos e fontes:** `02_TRABALHO/b2-fatos-stack-2026-11-03_v01/FICHA.md`. Verificações e achados no LOG de 20:52.
- **Para o B3:** o NAT é obrigatório, porque é a única saída da stack para a internet. Faltam também as Variables do GitHub, os 2 tokens do GitHub e os `TF_VAR_*` dos segredos.

## 24. Integração genérica configurada e sequência de avanço — 2026-11-04, Codex

Fonte: relato do usuário nesta data e conferência local da dev em 64d3af9. Usuário criou Events API V2, atualizou PAGERDUTY_INTEGRATION_KEY no .env e manteve PRTG. Considerar configuração concluída por relato, mas validação da nova chave pendente. O teste bem-sucedido de 2026-11-03 pertence à integração anterior. Não pedir que repita a criação.

O .env está ignorado pelo Git; foram conferidos apenas nomes de variáveis, sem exposição de valores. Chaves SaaS esperadas presentes. GITHUB_DISPATCH_TOKEN/GITHUB_TOKEN e equivalentes TF_VAR_github_dispatch_token/TF_VAR_github_token não aparecem nesse arquivo; nada foi concluído sobre existência dos tokens fora dele. TODO(human) de inject_fault() ainda existe; exercício do usuário preservado. Testes anteriores do B2 não foram reexecutados nesta orientação.

Próximo: concluir exercício e seus testes; validar nova integração e webhook Slack; disponibilizar tokens; preparar estimativa, orçamento e planos B3; após aprovação específica, implantar e promover dev → main; então demonstrar cadeia completa, registrar evidências e finalizar entrega. O teste direto do webhook Slack continua dependendo da autorização específica já pendente; nenhum evento ou mensagem foi enviado nesta consulta. OAuth do assistente não é pré-requisito de alertas. Sequência e fontes oficiais consultadas em 2026-11-04 no checkpoint de PENDENCIAS. Sem nova decisão de arquitetura, publicação ou operação AWS.

## 24. Preparação do B3 — 2026-11-04, Codex e Claude

- **Notificações reais com a nova Events API V2:** trigger e resolve `202`, webhook do Slack `200`, cartão até Resolved (Codex).
- **Testes:**
  - unitários dos 5 serviços;
  - ensaio integrado: 19 spans e 5 serviços na repetição;
  - New Relic sem falhas;
  - ensaio da falha proposital 11/11. O reinício limpa a falha, e o evaluation responde 502 em cascata.
- **Conta AWS:** plano FREE com US$ 100 até 2027-04-20, cota de 5 vCPUs (2 nós de 2 vCPU no máximo), nenhum Budget criado e 5 atividades de US$ 20.
- **Terraform:**
  - base com 8 import, 29 add, 7 change e 0 destroy;
  - o cluster se chama `togglemaster`, e `togglemaster-eks-cluster` é a role;
  - cluster e k8s dependem do apply da base.
- **Custo:** US$ 0,409/h = US$ 9,82/dia; B3–B5 ≈ US$ 45. Base parada com NAT: US$ 1,20/dia.
- **Roteiro:** `02_TRABALHO/PREPARACAO_B3_2026-11-04_v01.md`.

## 25. Pré-requisitos do B3 fechados — 2026-11-05, Claude

- **Tokens do GitHub:** os 2 são fine-grained e valem até 2027-01-04.
  - Os dois leem o repositório pela API e pelo git via HTTPS, como o ArgoCD.
  - O de disparo faz `repository_dispatch` (204).
  - O do ArgoCD também tem escrita; o usuário aceitou o risco (D-020).
- **Orçamento `togglemaster-creditos`:**
  - US$ 80 de custo acumulado de 2026-10-01 a 2027-04-30, sem contar créditos;
  - 5 alertas para 2 e-mails: gasto real em 25/50/75/100% e previsão em 100%;
  - fora do Terraform, para sobreviver ao `destroy`.
- **Créditos:** US$ 120 depois da atividade do Budgets. As atividades de EC2 e RDS ainda podem render US$ 20 cada, se a AWS reconhecer os recursos do B3.
- **Senha do PagerDuty:** mantida por decisão do usuário (D-020).
- **Próximo passo:** autorização dos tópicos 5 e 6.

## 26. Teste da confiança OIDC no CI — 2026-11-05, Claude

- `terraform/modules/iam-ci/tests/trust.tftest.hcl`, com 10 casos (commit b2c5bdf), roda no Terraform Check sem credencial. Cobre:
  - o subject exato da main;
  - a recusa de curingas;
  - a trust compartilhada pelas roles do CI e do self-healing;
  - as permissões mínimas das duas roles.
- O lock do módulo fixa o aws 6.62.0, o mesmo da camada base.
- O OIDC da conta nova já está configurado: provedor, role do CI com a trust exata, policy anexada e 3 Variables. O apply da base cria a role do self-healing; as Variables `AWS_SELF_HEALING_ROLE_ARN` e `EKS_CLUSTER_NAME` entram na etapa 2 do roteiro.
- O primeiro login OIDC real nesta conta acontece no job `image`, depois do merge na main.

## 27. Painel dos nós e cobertura do CI — 2026-11-05, Claude

- O dashboard `togglemaster-overview` tem 9 painéis desde o commit 46d0a18. Os novos mostram CPU e memória por nó, vindas do node-exporter, e atendem ao "uso de recursos do cluster" do enunciado (p. 3).
- A CPU usa tempo ocupado sobre tempo total medido. Assim o número continua certo mesmo onde os contadores do kernel não somam 1 por núcleo, como no Docker sobre WSL2.
- Os 3 eventos (push na dev, PR para a main e merge) rodam as mesmas verificações, filtradas por caminho. Imagem, OIDC, ECR e GitOps rodam só no merge.
- `gitops/**` e os scripts `test-restart.sh` e `security-check.sh` não têm verificação no CI (LOG 15:19).
