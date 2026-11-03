# Catálogo de achados — auditoria Codex 2026-10-30

TL;DR: 13 registros rastreáveis, dos quais 5 novos (F-027–F-031); F-023 confirmado corrigido no código local. Prioridade Alta significa bloqueio de entrega/publicação, não classificação de vulnerabilidade explorável.

Última atualização: 2026-10-30T16:00:11-03:00, Codex.

| ID | Prioridade | Natureza | Estado | Tema |
|---|---|---|---|---|
| [F-019](#f-019) | Alta | lacuna FIAP | Aberto | Observabilidade de cluster e ativação OTel ainda ausentes |
| [F-020](#f-020) | Média | qualidade de validação | Aberto | CI não executa a prova integrada de observabilidade |
| [F-021](#f-021) | Média | documentação/handoff | Aberto | Documentação vigente, backlog e plano não refletem o mesmo estado |
| [F-022](#f-022) | Média | dívida de validação | Aberto | Exceções de scanner com revisão vencida |
| [F-023](#f-023) | Informativa | correção confirmada | Resolvido no código local | Trust OIDC corrigida localmente; fechamento anterior estava pendente |
| [F-024](#f-024) | Alta | organização/publicação | Aberto | Log de 156 MB não ignorado pode impedir publicação Git |
| [F-025](#f-025) | Informativa | preservação/publicação | Aberto | Avanços ainda dependem da árvore local; exclusões preexistentes precisam de curadoria |
| [F-026](#f-026) | Média | incerteza externa | Aberto | Créditos AWS e continuidade do trial PagerDuty permanecem sem prova |
| [F-027](#f-027) | Média | defeito de configuração | Aberto | ArgoCD e HPA disputam spec.replicas |
| [F-028](#f-028) | Média | exposição local de configuração | Aberto | Laboratório publica bancos/cache e APIs sem restringir IP do host |
| [F-029](#f-029) | Média | lacuna de prevenção de regressão | Aberto | CI não renderiza nem valida o conjunto GitOps |
| [F-030](#f-030) | Média | lacuna de gatilhos CI | Aberto | Mudanças em políticas compartilhadas não disparam os scans por serviço |
| [F-031](#f-031) | Média | reprodutibilidade/isolamento | Aberto | Ensaios Compose herdam variáveis do terminal apesar da promessa de valores fictícios |

<a id="f-019"></a>
## F-019 — Observabilidade de cluster e ativação OTel ainda ausentes

**Alta · lacuna FIAP · Aberto**

**Evidência:** O overlay gera 23 objetos da aplicação/base, sem Collector/Prometheus/Loki/Grafana. O único helm_release operacional é ArgoCD. A configuração local tem somente pipeline traces com debug e arquivo; não tem pipelines metrics/logs nem exportador APM. Não há variáveis OTEL nos manifests GitOps dos cinco workloads.

**Fontes no snapshot:** `gitops/base/kustomization.yaml:34`; `gitops/overlays/prod/kustomization.yaml:65`; `observability/otel-collector-local.yaml:54`; `terraform/k8s/argocd.tf:94`.

**Impacto:** A base pode renderizar e os testes locais passar sem que a observabilidade obrigatória da Fase 4 exista no Kubernetes.

**Correção recomendada:** Adicionar charts/values ao GitOps; Collector de logs por nó e gateway conforme arquitetura escolhida; Prometheus, Loki, Grafana, rotas de sinais, configuração dos workloads e dashboard. Definir armazenamento, retenção, recursos e credenciais do exportador.

**Aceite:** ArgoCD saudável na conta correta; dados atuais dos cinco serviços e contêineres do cluster consultáveis; dashboard mostra recursos, requisições e logs; trace e mapa aparecem no APM.

**Relação FIAP:** REQ-OBR-06, REQ-OBR-07, REQ-OBR-08, REQ-OBR-09, REQ-OBR-10, REQ-OBR-11, REQ-OBR-14, REQ-OBR-15, REQ-OBR-20. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Reconfirma F-019 e I-01/I-02 da revisão de 2026-10-28. Não é uma regressão causada pelo Claude.

**Limite da conclusão:** Ausência nos fontes operacionais locais; não foi feito inventário de todo recurso remoto nesta rodada.

<a id="f-020"></a>
## F-020 — CI não executa a prova integrada de observabilidade

**Média · qualidade de validação · Aberto**

**Evidência:** Compose Integration chama somente test-compose.sh; diagnóstico e limpeza usam dois arquivos Compose. Nenhum dos nove workflows chama test-observability.sh/test-traces.py. A publicação depende de build/lint/SAST/SCA do próprio workflow; a integração fica em outro workflow.

**Fontes no snapshot:** `.github/workflows/compose-integration.yml:22`; `scripts/test-observability.sh:17`; `scripts/integration/test-traces.py:194`; `.github/workflows/_ci-go.yml:326`; `.github/workflows/_ci-python.yml:359`.

**Impacto:** Uma regressão no Collector, correlação HTTP/SQS ou sanitização pode passar no fluxo remoto atual. Não há dependência explícita entre publicação e aprovação do ensaio integrado.

**Correção recomendada:** Incluir a prova OTel e seus três overlays no CI; preservar evidência sanitizada. Definir como os checks obrigatórios de PR/publicação impedirão uma entrega com integração falhando.

**Aceite:** Uma falha deliberada e controlada no contrato de traces reprova o CI; a limpeza inclui o Collector. Confirmar gates remotos após publicação autorizada.

**Relação FIAP:** REQ-OBR-04, REQ-OBR-13, REQ-OBR-14, REQ-OBR-21, REQ-OBR-23. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Reconfirma F-020/I-06; acrescenta a separação dos workflows como ponto de aceite.

**Limite da conclusão:** O PDF exige CI/CD e evidência, mas não nomeia esse teste específico. Não foram consultadas regras atuais de proteção de branch.

<a id="f-021"></a>
## F-021 — Documentação vigente, backlog e plano não refletem o mesmo estado

**Média · documentação/handoff · Aberto**

**Evidência:** README/Terraform ainda tratam a conta como não informada; observability/README diz que não há conta New Relic. Registros de 2026-10-28/30 já trazem conta/Variables conferidas, contas externas relatadas e backend.hcl criado. SECURITY afirma trust para qualquer branch/PR, contradizendo StringEquals/main atual. Catálogo normativo segue todo Pendente. Há três âncoras quebradas nos dez Markdown operacionais verificados. Plano v02 preserva cronograma de setembro e instrumentadores planejados diferentes da execução registrada.

**Fontes no snapshot:** `README.md:5`; `terraform/README.md:3`; `observability/README.md:83`; `SECURITY.md:20`; `docs/requisitos/README.md:14`; `gitops/SECRETS-CONTRATO.md:10`; `docs/ARQUITETURA.md:7`; `docs/GUIA_DE_REPRODUCAO.md:9`.

**Impacto:** O próximo agente pode repetir cadastro ou a correção OIDC, seguir comandos da conta anterior, ou confundir plano com entrega. O guia histórico contém merge/push diretos para main e init sem backend-config; não serve como runbook vigente do 04.

**Correção recomendada:** Atualizar README/SECURITY/runbook e produzir nova versão do plano, preservando as anteriores. Usar esta matriz para execução e o catálogo original como fonte normativa. Corrigir os três links e fechar o registro de P-013 sem repetir trabalho.

**Aceite:** Um leitor de LOG+PENDENCIAS identifica claramente o ponto atual, inclusive conta verificada em 28, backend criado em 30 e integrações ainda não validadas. Documentos operacionais não mandam refazer F-023.

**Relação FIAP:** REQ-OBR-23, REQ-OBR-39, REQ-OBR-40, REQ-OBR-42. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Reconfirma F-021/DOC-01 a DOC-05; amplia de duas para três âncoras porque incluiu SECRETS-CONTRATO. Estado posterior do Claude incorporado.

**Limite da conclusão:** Correções desta rodada limitadas ao contexto e às saídas da auditoria; os documentos operacionais ficam como achados, sem edição.

<a id="f-022"></a>
## F-022 — Exceções de scanner com revisão vencida

**Média · dívida de validação · Aberto**

**Evidência:** As três exceções CVE têm revisão marcada para 2026-10-15; a auditoria é de 2026-10-30. Os quatro scans usam esse arquivo.

**Fontes no snapshot:** `.trivyignore:58`; `.github/workflows/_ci-go.yml:309`; `.github/workflows/_ci-python.yml:342`.

**Impacto:** O gate pode continuar suprimindo achados com justificativas de imagens de setembro, sem confirmação sobre o artefato final.

**Correção recomendada:** Reexecutar os scans das imagens/dependências finais na revisão das aplicações e revisar cada exceção, correção disponível, exposição e prazo.

**Aceite:** Cada exceção retida tem evidência recente e justificativa; os scans finais e seu resultado são preservados.

**Relação FIAP:** REQ-OBR-04. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Reconfirma F-022/I-08. Nenhum CVE novo foi atribuído ao projeto.

**Limite da conclusão:** Código, imagens e dependências dos cinco serviços estão fora do escopo atual. Data vencida não comprova vulnerabilidade explorável.

<a id="f-023"></a>
## F-023 — Trust OIDC corrigida localmente; fechamento anterior estava pendente

**Informativa · correção confirmada · Resolvido no código local**

**Evidência:** Subject usa owner/repo e seus IDs imutáveis, branch main e StringEquals para sub/aud. Os três arquivos do módulo são byte a byte idênticos ao harness que registrou 8 testes aprovados em 2026-10-28. Correspondência AWS/GitHub registra 34 checks verdadeiros em 28. Terraform validate atual passou.

**Fontes no snapshot:** `terraform/modules/iam-ci/main.tf:80`; `terraform/modules/iam-ci/main.tf:139`; `terraform/modules/iam-ci/variables.tf:23`; `terraform/variables.tf:189`; `00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/correspondencia-aws-github.json:1`.

**Impacto:** Não refazer a correção nem aplicar a versão antiga; a pendência real é documental/publicação futura e validação de OIDC em workflow real.

**Correção recomendada:** Usar o subject atual. Atualizar status de P-013/F-023 e, quando autorizado o fluxo remoto, provar autenticação e push ECR.

**Aceite:** Relatório da etapa 9 ligado ao contexto; CI remoto autentica apenas no contexto esperado. Consultar configuração novamente se owner/repo/branch/environment mudar.

**Relação FIAP:** REQ-OBR-04. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Concorda com Claude em 2026-10-28 15:11. Contradiz apenas caixas/TL;DR antigos ainda não atualizados.

**Limite da conclusão:** 34/34 e 8/8 são evidências de 2026-10-28, reabertas e comparadas; não foram reexecutadas na AWS em 30.

<a id="f-024"></a>
## F-024 — Log de 156 MB não ignorado pode impedir publicação Git

**Alta · organização/publicação · Aberto**

**Evidência:** offline-test.jsonl tem 156400265 bytes (149,15 MiB), está não rastreado e git check-ignore retorna 1. O gerador usa terraform test -json -verbose e salva a saída integral. O resumo confirma 8 passed/0 failed; o volume não é necessário para apresentar o resultado.

**Fontes no snapshot:** `00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/terraform/test-oidc-offline.py:139`; `.gitignore:1`.

**Impacto:** Um git add indiscriminado inclui arquivo maior que o limite de 100 MiB do GitHub para Git comum.

**Correção recomendada:** Antes de qualquer commit, ignorar especificamente o artefato bruto e preservar resumo sanitizado/hashes; decidir retenção/arquivamento do bruto. Remover -verbose quando não necessário para evitar nova geração gigante.

**Aceite:** git check-ignore reconhece o bruto e a seleção de arquivos para commit não o contém; resumo dos testes continua acessível.

**Relação FIAP:** REQ-OBR-20, REQ-OBR-21, REQ-OBR-22. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Concorda e mede precisamente o F-024 do Claude; não apagado nem modificado.

**Limite da conclusão:** Não houve commit/push. Não é pedido para usar LFS para log temporário.

Documentação primária consultada em 2026-10-30: [fonte 1](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

<a id="f-025"></a>
## F-025 — Avanços ainda dependem da árvore local; exclusões preexistentes precisam de curadoria

**Informativa · preservação/publicação · Aberto**

**Evidência:** Snapshot na dev, HEAD 3b21e65d8b22c454e43ba7dc3b3eb3a039ea061e, main 003a7075a8908011ece83d317d5c700ac2525b58. Instrumentação/Collector/trust e outros avanços estão fora do último commit. Há 34 caminhos rastreados ausentes: as 33 exclusões antigas de aulas Fase 3 e docs/POSTECH - Tech Challenge - Fase 3.pdf.

**Fontes no snapshot:** `00_COLAB_IA/02_TRABALHO/auditoria-codex-2026-10-30_v01/git-status-inicial.txt:1`; `00_COLAB_IA/02_TRABALHO/auditoria-codex-2026-10-30_v01/inventario-inicial.json:1`.

**Impacto:** Outro clone/ArgoCD não recebe esses avanços. Publicar a árvore inteira sem curadoria pode incluir exclusões e artefatos indevidos.

**Correção recomendada:** Preservar a árvore e selecionar conscientemente o que comporá um commit quando o usuário autorizar. Não restaurar/apagar as exclusões por suposição; comparar com snapshot da auditoria antes do merge/PR.

**Aceite:** Revisão de git diff e da lista do índice, com preservação dos materiais da Fase 4; publicação futura via fluxo autorizado dev → PR → main.

**Relação FIAP:** REQ-OBR-20, REQ-OBR-21, REQ-OBR-22, REQ-OBR-34. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Concorda com F-025, atualiza 33 para 34 ausências já presentes no início desta rodada.

**Limite da conclusão:** Não commitar é compatível com a instrução do usuário. Isto é risco de preservação e diferença entre local/remoto, não falha disciplinar do agente.

<a id="f-026"></a>
## F-026 — Créditos AWS e continuidade do trial PagerDuty permanecem sem prova

**Média · incerteza externa · Aberto**

**Evidência:** Etapa 8 não consultou Billing/créditos/cotas. Claude registra 12 dias de trial PagerDuty restantes em 2026-10-30, término aproximado 2026-11-11; data exata não conferida na conta. Contas New Relic/Slack/PagerDuty já foram relatadas como criadas. A página pública atual lista Free e integrações/APIs, enquanto a linha de franquia Events da plataforma diz Not included.

**Fontes no snapshot:** `00_COLAB_IA/_ARQUIVO_MORTO/2026-10-30_auditoria-codex/LOG_DE_TRABALHO.md:13`; `00_COLAB_IA/02_TRABALHO/etapas8-9-2026-10-28_v01/aws/PARECER_AWS_ETAPA8.md:64`.

**Impacto:** Provisionar ou adiar a demonstração apoiado em benefício presumido pode gerar custo ou perda de uma capacidade usada no ensaio.

**Correção recomendada:** Conferir plano/créditos/cotas AWS e término/plano efetivo do PagerDuty. Priorizar ensaio completo antes do término informado. Confirmar especificamente Events API/integrador utilizado após trial, sem inferir indisponibilidade absoluta da linha isolada da tabela.

**Aceite:** Evidência datada de conta/plano/limites e teste da integração dentro do plano efetivamente disponível; prazo de gravação definido com margem.

**Relação FIAP:** REQ-OBR-03, REQ-OBR-12, REQ-OBR-17, REQ-OBR-30. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Concorda com cautela F-026 e risco de calendário. ⚠️ CONFLITO interpretativo não bloqueante: o registro Claude lê a linha Events como risco de indisponibilidade; Codex não a considera suficiente para afirmar que toda integração Events API do Free termina. Manter [INCERTO] até confirmação da conta/suporte.

**Limite da conclusão:** Não foi consultada conta SaaS/Billing nesta rodada. Não afirmar elegibilidade nem impossibilidade de usar Free; não propor recriar contas para obter benefícios.

Documentação primária consultada em 2026-10-30: [fonte 1](https://www.pagerduty.com/pricing/).

<a id="f-027"></a>
## F-027 — ArgoCD e HPA disputam spec.replicas

**Média · defeito de configuração · Aberto**

**Evidência:** Os dois Deployments declaram replicas: 1; HPAs podem elevar para 2. A Application ativa automated/selfHeal e não define ignoreDifferences/RespectIgnoreDifferences para réplicas. Render atual confirma os dois pares.

**Fontes no snapshot:** `gitops/base/evaluation-service/deployment.yaml:26`; `gitops/base/analytics-service/deployment.yaml:24`; `gitops/base/evaluation-service/hpa.yaml:35`; `gitops/base/analytics-service/hpa.yaml:31`; `terraform/k8s/argocd.tf:315`.

**Impacto:** Quando HPA aumentar réplicas, ArgoCD pode identificar desvio e reconciliar para 1, provocando oscilação ou reduzindo capacidade durante carga.

**Correção recomendada:** Definir o HPA como responsável por réplicas desses dois Deployments: remover o campo do desejado quando apropriado, ou configurar ignoreDifferences restrito aos dois nomes e RespectIgnoreDifferences=true. Não ignorar réplicas de todos os workloads indiscriminadamente.

**Aceite:** Em ensaio de carga no cluster, HPA mantém 2 réplicas durante sincronização ArgoCD, inclusive sync de outra alteração; demais campos seguem reconciliados.

**Relação FIAP:** REQ-OBR-01, REQ-OBR-05. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Novo nesta rodada; não localizado nos relatórios anteriores examinados.

**Limite da conclusão:** Configuração e comportamento documentado confirmados; oscilação não observada em cluster nesta sessão. HPA não é requisito novo da Fase 4, mas faz parte da base importada.

Documentação primária consultada em 2026-10-30: [fonte 1](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/#respect-ignore-differences-configs).

<a id="f-028"></a>
## F-028 — Laboratório publica bancos/cache e APIs sem restringir IP do host

**Média · exposição local de configuração · Aberto**

**Evidência:** Nove portas publicadas não têm host_ip: PostgreSQL 5433/5434, Redis 6379, DynamoDB 8000 e aplicações 8001–8005. Compose config confirma; somente portas do Collector estão em 127.0.0.1. O ambiente usa credenciais fictícias conhecidas e Redis sem autenticação configurada no Compose.

**Fontes no snapshot:** `docker-compose.yaml:14`; `docker-compose.yaml:35`; `docker-compose.yaml:56`; `docker-compose.yaml:69`; `.env.example:22`; `.env.example:34`.

**Impacto:** No padrão do Docker, a publicação alcança interfaces do host além de loopback; outros clientes da rede podem acessar o laboratório quando firewall/roteamento permitirem.

**Correção recomendada:** Restringir publicações necessárias a 127.0.0.1 e remover publicações de dados que só precisam de acesso entre contêineres.

**Aceite:** Configuração normalizada e inspeção de sockets mostram apenas loopback para portas locais necessárias; testes via localhost continuam funcionando.

**Relação FIAP:** REQ-OBR-04. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Novo nesta rodada; recomendação de segurança do laboratório, não obrigação literal da FIAP.

**Limite da conclusão:** Não foram iniciados contêineres nem testada exposição real da máquina à rede/internet.

Documentação primária consultada em 2026-10-30: [fonte 1](https://docs.docker.com/engine/network/port-publishing/).

<a id="f-029"></a>
## F-029 — CI não renderiza nem valida o conjunto GitOps

**Média · lacuna de prevenção de regressão · Aberto**

**Evidência:** A renderização kubectl kustomize só existe no script local opcional. Terraform Check é filtrado por terraform/**; o job GitOps usa edit set image, não build/validação do conjunto. Nenhum dos nove workflows chama validate-all.sh ou renderiza o overlay.

**Fontes no snapshot:** `.github/workflows/compose-integration.yml:22`; `.github/workflows/terraform-check.yml:30`; `scripts/validate-all.sh:53`; `.github/workflows/_ci-go.yml:583`; `.github/workflows/_ci-python.yml:613`.

**Impacto:** Um PR que altera apenas manifests pode passar no Compose e introduzir referência/estrutura GitOps quebrada, descoberta só na sincronização.

**Correção recomendada:** Adicionar check local de renderização e validação de schema/contratos de manifests ao CI para mudanças em gitops/** e configuração de charts. Fazer o check requerido no fluxo de revisão.

**Aceite:** Um caso controlado com recurso inexistente no kustomization reprova o check; configuração válida renderiza todos os objetos sem acesso ao cluster.

**Relação FIAP:** REQ-OBR-04, REQ-OBR-05, REQ-OBR-20. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Novo nesta rodada; distinto de F-020 (regressão de telemetria).

**Limite da conclusão:** O estado atual renderizou corretamente; o achado é ausência do gate remoto, não YAML quebrado hoje.

<a id="f-030"></a>
## F-030 — Mudanças em políticas compartilhadas não disparam os scans por serviço

**Média · lacuna de gatilhos CI · Aberto**

**Evidência:** Os filtros push/pull_request listam apenas a pasta do serviço, o workflow chamador e o reutilizável. .trivyignore é consumido por ambos os reutilizáveis e .pylintrc pelo Python, mas nenhum dos dois aparece nesses filtros.

**Fontes no snapshot:** `.github/workflows/auth-service.yml:45`; `.github/workflows/analytics-service.yml:44`; `.github/workflows/evaluation-service.yml:44`; `.github/workflows/flag-service.yml:44`; `.github/workflows/targeting-service.yml:44`; `.github/workflows/_ci-python.yml:229`.

**Impacto:** Alterar só exceções Trivy ou configuração Pylint não reexecuta os jobs que consomem a política, reduzindo a evidência de revisão do controle.

**Correção recomendada:** Incluir os arquivos compartilhados pertinentes nos filtros ou usar um workflow agregador que determine os serviços afetados; manter build/publicação separados das verificações de política.

**Aceite:** PR somente com alteração em .trivyignore roda scans aplicáveis; PR em .pylintrc roda lint dos três serviços Python, sem publicar imagens em PR/dev.

**Relação FIAP:** REQ-OBR-04. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Novo nesta rodada; confirmado pela leitura dos cinco chamadores.

**Limite da conclusão:** Não foi disparado workflow nem verificada proteção remota da branch.

<a id="f-031"></a>
## F-031 — Ensaios Compose herdam variáveis do terminal apesar da promessa de valores fictícios

**Média · reprodutibilidade/isolamento · Aberto**

**Evidência:** Scripts limpam SERVICE_API_KEY, mas mantêm MASTER_KEY, DATABASE_URLs, senhas e portas herdadas. Reprodução só com docker compose config e MASTER_KEY sintética no subprocesso confirmou que o valor do terminal sobrepõe .env.example. Os testes usam a chave local fixa.

**Fontes no snapshot:** `scripts/test-compose.sh:11`; `scripts/test-observability.sh:12`; `docker-compose.yaml:82`; `scripts/integration/test-flow.py:51`; `scripts/integration/test-traces.py:158`.

**Impacto:** O ensaio pode falhar com autenticação/portas diferentes e pode colocar parâmetros reais herdados no laboratório. URLs de banco herdadas também podem direcionar conexões fora da composição pretendida.

**Correção recomendada:** Isolar o ambiente dos ensaios: sobrescrever explicitamente todas as entradas relevantes com os valores fictícios e validar endpoints/portas; preservar somente variáveis de controle permitidas, como identidade/pasta QA.

**Aceite:** Teste de configuração com sentinelas host para MASTER_KEY/URLs/portas confirma que elas não chegam à composição; ensaio continua usando somente dependências locais.

**Relação FIAP:** REQ-OBR-01, REQ-OBR-23. Não transformar recomendação de implementação em obrigação adicional.

**Comparação:** Novo nesta rodada, com reprodução isolada em validacoes/repro-ambiente-compose.json.

**Limite da conclusão:** Nenhum segredo real foi exibido/salvo; nenhum contêiner ou conexão a banco foi iniciado. O efeito em configuração foi reproduzido, não um vazamento ocorrido.

Documentação primária consultada em 2026-10-30: [fonte 1](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/).
