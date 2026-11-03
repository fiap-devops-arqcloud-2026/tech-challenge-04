# Revisão geral — infraestrutura, GitOps e CI/CD da Fase 4

TL;DR: a base importada possui Terraform organizado, manifests dos cinco serviços e CI/CD com etapas DevSecOps. A validação estática executada em 2026-10-27 passou nas três raízes Terraform e renderizou 23 objetos Kubernetes. Isso não comprova implantação na nova conta. A stack de observabilidade, sua configuração no cluster, os alertas e a automação de incidentes continuam ausentes dos arquivos operacionais examinados. As imagens, endpoints e roles do overlay ainda são marcadores de conta pendente.

Última atualização: 2026-10-28 09:09, America/Sao_Paulo (UTC-03:00), Codex — revisão independente de infraestrutura. Inspeção iniciada em 2026-10-27; retomada documental em 2026-10-28, sem repetir testes.

## 1. Escopo e método

Revisão local de `terraform/`, `gitops/`, `.github/workflows/`, `infra/`, scripts de validação e documentos operacionais relacionados. Leitura cruzada com `docs/requisitos/README.md`, que referencia o enunciado, p. 2–6. A conferência integral do PDF e a matriz dos 42 itens são responsabilidade da revisão principal.

Foram separados três níveis: **código/configuração existente**, **validação estática local** e **funcionamento implantado**. A ausência de evidência remota nesta revisão não prova que um recurso não exista em alguma conta. Nenhuma identidade, cobrança, estado remoto, imagem ECR, execução GitHub Actions ou cluster foi consultado.

Não houve alteração de código/configuração, `init`, `plan`, `apply`, publicação, envio de alerta ou operação AWS. A análise não é uma auditoria completa de vulnerabilidades. Não foram pesquisados CVEs atuais nem modificadas exceções de scanners.

## 2. O que já existe

| Área | Implementação encontrada | Limite da conclusão |
|---|---|---|
| Terraform base | Rede/VPC, ECR para os cinco serviços, SQS/DLQ, DynamoDB e identidade OIDC do CI. | Declarações em código; sem inventário de recursos ativos. |
| Terraform cluster | EKS/node group, dois RDS, ElastiCache, IRSA, addons de rede, DNS, EBS CSI e metrics-server. | Não constitui a stack Prometheus/Loki/Grafana exigida na Fase 4. |
| Terraform Kubernetes | Namespace, Secrets, StorageClass gp3, instalação Helm do ArgoCD e Application para o repositório 04. | Os charts de observabilidade não foram adicionados; a Application aponta para publicação futura na `main`. |
| GitOps | Cinco Deployments/Services de aplicação, ConfigMaps, duas ServiceAccounts IRSA, dois HPAs e PostgreSQL targeting com PVC. | Runtime ainda depende de conta, imagens, endpoints, schemas e seed reais. |
| CI/CD | Cinco workflows por serviço, dois reutilizáveis Go/Python, Terraform Check e Compose Integration: nove workflows. | Arquivos presentes não comprovam execução remota atual. |
| DevSecOps | Linters, gosec/Bandit, Trivy de dependências/imagens, bloqueio dos jobs de publicação pelos jobs anteriores; OIDC para ECR. | Scans precisam ser executados sobre os artefatos finais; exceções têm revisão vencida. |

Fontes: `terraform/main.tf:45`, `terraform/cluster/main.tf:45`, `terraform/modules/eks/main.tf:66`, `terraform/modules/eks/main.tf:317`, `terraform/k8s/argocd.tf:94`, `gitops/base/kustomization.yaml:34`, `.github/workflows/_ci-go.yml:70`, `.github/workflows/_ci-python.yml:69`.

Há 40 arquivos `.tf`, sete diretórios de módulos locais e três raízes independentes. As camadas são `base`, `cluster` e `k8s`, não três ambientes. As chaves de estado são `phase4/prod/base.tfstate`, `phase4/prod/cluster.tfstate` e `phase4/prod/k8s.tfstate` (`terraform/backend.tf:43`, `terraform/cluster/backend.tf:47`, `terraform/k8s/backend.tf:55`).

## 3. Lacunas prioritárias e critérios de encerramento

### I-01 — Stack de observabilidade ainda não declarada no GitOps

**Requisitos afetados:** REQ-OBR-06–10, 20, 25–26; enunciado p. 3, 5.

O overlay renderizado contém 23 objetos: seis ConfigMaps, cinco Deployments, dois HPAs, um Namespace, seis Services, duas ServiceAccounts e um StatefulSet. Não contém Collector, Prometheus, Loki ou Grafana. O único `helm_release` examinado é o ArgoCD (`terraform/k8s/argocd.tf:94`). O conjunto operacional não possui valores/charts de observabilidade, dashboards ou regras de alerta.

**Falta:** acrescentar os charts/valores ao GitOps, configurar armazenamento e retenção, permissões/coleta e fontes de dados; implantar e comprovar métricas de infraestrutura, logs dos contêineres do cluster e visualização principal no Grafana. O dashboard deverá incluir uso de recursos, taxa de requisições e logs em tempo real. A escolha de charts, retenção e dimensionamento é implementação do projeto, não uma quantidade de recursos prescrita pelo PDF.

### I-02 — Publicar imagens instrumentadas não ativa OTel no Kubernetes atual

**Requisitos afetados:** REQ-OBR-11, 14–15, 20–21, 27; enunciado p. 4–6.

Não há endpoint/configuração OTel nos ConfigMaps e Deployments de `gitops/base/` nem no overlay `prod`. A instrumentação é opt-in: `services/auth-service/telemetry.go:39` retorna sem SDK quando os endpoints estão vazios, e `services/flag-service/telemetry.py:73` faz a mesma verificação. Os outros serviços seguem a implementação local correspondente.

**Falta:** configurar identidade/ambiente e endpoint OTLP nos cinco workloads, instalar o Collector acessível no cluster, adicionar pipelines de métricas/logs/traces e os destinos Prometheus/Loki/APM. Preservar o tratamento de atributos existente ao implementar o exportador New Relic. Provar a ingestão, o trace de `/evaluate` e o mapa dos cinco serviços no APM. A evidência local de 19 spans não substitui essa prova externa.

### I-03 — Conta, backend e overlay ainda não estão prontos para implantação

**Requisitos afetados:** REQ-OBR-01, 03–05, 20, 23, 25; enunciado p. 2, 5.

Na inspeção de 2026-10-27 não foram encontrados `backend.hcl`, `terraform.tfvars` ou `terraform.tfstate` reais nas três raízes. Variáveis de ambiente e estado remoto não foram investigados. Os exemplos preservam `CONTA_AWS_PENDENTE`/`NOVO_BUCKET_ESTADO_FASE4`.

O GitOps contém cinco imagens `registry.conta-pendente.invalid`, tags `conta-pendente` (`gitops/overlays/prod/kustomization.yaml:65`), Redis e fila com domínio `.invalid` (`patches/endpoints.yaml:31`, `:39`, `:49`) e duas roles com conta pendente (`patches/irsa.yaml:31`, `:43`). São sentinelas intencionais, não endpoints que possam operar.

**Falta:** confirmar identidade, região, orçamento/cotas, criar/configurar backend próprio, preencher parâmetros das três camadas e substituir os marcadores pelos outputs confirmados. Não transportar state ou segredos da Fase 3. Revalidar as configurações dos serviços quando a região mudar; `AWS_REGION` em `gitops/base/analytics-service/configmap.yaml:25` e `evaluation-service/configmap.yaml:32` permanece `us-east-2`.

`allowed_account_ids` existe nos providers AWS, mas backend S3, `terraform_remote_state` e `exec` da AWS CLI são configurações separadas. A conferência de identidade deve abranger esses caminhos; não presumir que o guard do provider cubra automaticamente o token Kubernetes (`terraform/k8s/providers.tf:18`, `:47`, `:77`; `terraform/k8s/data.tf:16`, `:34`).

### I-04 — Bootstrap e seed precisam integrar o roteiro vigente da Fase 4

**Requisitos afetados:** REQ-OBR-01, 03, 05, 23, 25; enunciado p. 2, 5.

O primeiro bootstrap do ArgoCD tem duas etapas documentadas: primeiro disponibilizar o chart/CRD e depois a Application. O comentário de `terraform/k8s/argocd.tf:228` explica por que a validação do CRD pelo `kubernetes_manifest` pode impedir um plan único em cluster novo; a receita existente está em `:249`–`:253`.

RDS auth/flag nascem sem schemas da aplicação. A chave `SERVICE_API_KEY` gerada em `terraform/k8s/secrets.tf:223` é provisória, não cadastrada no auth. O seed deve criar a chave real e atualizar o Secret; `ignore_changes` em `:256` preserva essa alteração. O PostgreSQL targeting tem inicialização própria por ConfigMap/StatefulSet.

**Falta:** produzir/adaptar um runbook vigente do 04 para bootstrap, schemas, chave e carga de exemplo, seguido de teste funcional completo no cluster. O contrato `gitops/SECRETS-CONTRATO.md:52` remete ao guia importado, que se identifica como histórico logo na primeira linha. Seus mecanismos são úteis como referência, mas os valores da conta anterior não devem ser executados. Referências históricas: `docs/GUIA_DE_REPRODUCAO.md:482`–`:540`.

### I-05 — Alerta, incidentes, ChatOps e automação ainda faltam

**Requisitos afetados:** REQ-OBR-16–19, 22, 28–31; enunciado p. 5–6.

Não foram encontradas regras operacionais de alerta ou integrações PagerDuty/Slack nos diretórios examinados, nem workflow de self-healing por `repository_dispatch`. São escolhas planejadas, não uma cadeia executável comprovada.

O `selfHeal = true` do ArgoCD (`terraform/k8s/argocd.tf:325`) reconcilia desvio do estado declarado. Ele não demonstra uma automação acionada pelo alerta da aplicação e não encerra REQ-OBR-19.

**Falta:** definir o problema proposital e o sinal, criar alerta, abertura de incidente/acionamento do responsável, ChatOps e a ação corretiva. Verificar a recuperação após a ação e reunir evidências do ciclo completo. Limitação de repetição, escopo da ação e prevenção de loops são sugestões de implementação do projeto, não exigências textuais adicionais da FIAP.

### I-06 — A prova integrada de OTel ainda não faz parte do CI

**Requisitos relacionados:** REQ-OBR-04, 13–14, 21 e 23. A inclusão desse teste específico no CI é recomendação técnica, não uma exigência nominal do PDF.

`.github/workflows/compose-integration.yml:22` chama somente `bash scripts/test-compose.sh`. Status/logs/limpeza usam apenas os dois arquivos Compose antigos (`:25`, `:28`, `:31`). Não há referência a `test-observability.sh`, `test-traces.py` ou `docker-compose.otel.yaml` em nenhum dos nove workflows.

**Falta recomendado:** integrar a validação do Collector e a prova HTTP/SQL/SQS/privacidade ao pipeline, incluindo os três overlays no diagnóstico/limpeza e preservando evidência sanitizada. Sem isso, uma regressão específica de tracing pode passar pelo ensaio funcional. Os testes unitários novos serão alcançados pelos jobs Go/Python quando forem publicados; o teste integrado OTel é uma lacuna distinta.

### I-07 — Dimensionamento e comentários herdados precisam de reconciliação documental

**Requisitos relacionados:** REQ-OBR-03, 05–11 e 23. Não há aqui evidência de que três workers sejam obrigação da FIAP.

`terraform/cluster/variables.tf:95`–`:102` mantém dois workers desejados, enquanto o plano da Fase 4 propõe três. Os defaults de versão/tipo e a topologia de dois RDS + banco targeting no cluster foram herdados. O texto das variáveis de módulos ainda contém afirmações da conta anterior, como a recusa de uma terceira instância (`terraform/modules/rds/variables.tf:31`) e restrições Free Tier (`terraform/modules/eks/variables.tf:30`). Não são comprovação da nova conta.

**Falta:** dimensionar aplicação + stack de observabilidade com base nos recursos/limites escolhidos, conferir cotas, disponibilidade e orçamento, e alinhar os documentos vigentes. Não alterar quantidade de nós somente para fazer o código coincidir com uma proposta antiga.

### I-08 — Exceções do Trivy precisam de reavaliação antes da entrega

**Requisito relacionado:** REQ-OBR-04; enunciado p. 2.

`.trivyignore:58` registra revisão prevista para **2026-10-15**, anterior à data desta revisão. As justificativas e as medições declaradas são históricas. Não foi feita consulta externa sobre validade, correção ou gravidade atual dos CVEs, nem novo scan de imagens.

**Falta:** executar os scans previstos sobre as dependências e imagens finais, revisar cada exceção com evidência atual e registrar a decisão. Não interpretar este apontamento como confirmação de uma vulnerabilidade atual ou como autorização para remover exceções sem análise.

## 4. Publicação e GitOps

O destino está corretamente adaptado ao repositório 04: `terraform/variables.tf` define `fiap-devops-arqcloud-2026/tech-challenge-04`; `terraform/k8s/variables.tf` define a URL do 04 e branch `main`. A Application lê esses valores em `terraform/k8s/argocd.tf:289`–`:301`.

Os workflows validam `dev`/PR, mas os jobs de imagem/GitOps só executam em push na `main` (`_ci-go.yml:331`, `:494`; `_ci-python.yml:364`, `:524`). As variáveis `AWS_REGION`, `ECR_REGISTRY` e `AWS_ROLE_ARN` configuram o destino; há verificação de consistência antes da autenticação/publicação. O bot atualiza tags na `main`; a publicação humana continua dependendo do fluxo autorizado pelo usuário.

**Falta:** publicar os fontes/configurações finais pelo fluxo aprovado, validar os pipelines do 04 e comprovar sincronização saudável + funcionamento da aplicação. A revisão atual não autoriza push, PR, merge, publicação de imagens ou implantação. Nenhuma execução remota foi consultada. Não confundir a existência de arquivos na `dev` local com o conteúdo que um ArgoCD remoto consegue ler.

## 5. Validações executadas e evidências

Executadas em **2026-10-27, aproximadamente 22:32, UTC-03:00**. Em 2026-10-28 apenas foram reabertos os arquivos resultantes para consolidar este relatório.

| Verificação | Resultado | Evidência |
|---|---|---|
| `terraform fmt -check -recursive terraform` | Saída 0, sem texto de erro. | Resultado da chamada de ferramenta da sessão; não foi gerado arquivo de log vazio. |
| `terraform -chdir=terraform validate -json` | `valid=true`, zero erros/avisos. | `qa-revisao-infra-2026-10-27/terraform-validate.json` |
| `terraform -chdir=terraform/cluster validate -json` | `valid=true`, zero erros/avisos. | `qa-revisao-infra-2026-10-27/terraform-cluster-validate.json` |
| `terraform -chdir=terraform/k8s validate -json` | `valid=true`, zero erros/avisos. | `qa-revisao-infra-2026-10-27/terraform-k8s-validate.json` |
| `kubectl kustomize gitops/overlays/prod` | Saída 0, 23 objetos. | `qa-revisao-infra-2026-10-27/gitops-renderizado.yaml` |

Os validates usaram os caches locais já existentes. Não houve init, atualização de provider/lockfile ou plan. O render Kustomize não contacta cluster. Nenhuma dessas verificações comprova existência de imagens, autenticação IRSA, seed, conexão a banco, APM ou observabilidade em funcionamento.

Uma tentativa auxiliar de consolidar inventário/parse YAML em Python parou por ausência de `yaml` no runtime escolhido; não produziu o JSON planejado, não instalou pacotes e não reduz o resultado do render Kustomize. Não alegar que os nove workflows passaram por esse parser nesta revisão. Eles foram inspecionados textualmente.

## 6. Inventário efetivamente examinado

- **40 arquivos `.tf`**: as três raízes `terraform/`, `terraform/cluster/`, `terraform/k8s/` e os sete módulos `ecr`, `eks`, `elasticache`, `iam-ci`, `irsa`, `messaging`, `rds`. Inspeção dos blocos executáveis, variáveis, outputs e comentários pertinentes; sem leitura do código interno dos providers ou de todo o módulo VPC baixado em `.terraform`.
- **Seis exemplos de configuração**: `backend.hcl.example` e `terraform.tfvars.example` de cada raiz. Também `.terraform.lock.hcl` das três raízes e `terraform/.gitignore`.
- **27 YAMLs GitOps**: `base/kustomization.yaml`, `base/namespace.yaml`; deployment/service/configmap dos cinco serviços; HPA/serviceaccount de evaluation e analytics; configmap/service/statefulset de postgres-targeting; `overlays/prod/kustomization.yaml` e patches endpoints/IRSA. O render reúne 23 objetos, pois kustomizations e patches não são novos objetos adicionais.
- **Nove workflows**: `_ci-go.yml`, `_ci-python.yml`, `terraform-check.yml`, `compose-integration.yml` e os cinco arquivos por serviço.
- **Scripts/configurações auxiliares**: `scripts/validate-all.sh`, `scripts/security-check.sh`, `infra/postgres-app/01-init-multi-db.sh`, `.gitignore`, `.trivyignore`, `.pylintrc`, `pyproject.toml`.
- **Documentos relacionados**: protocolo/backlog/decisões da colaboração, README de requisitos, `terraform/README.md`, `gitops/README.md`, `gitops/SECRETS-CONTRATO.md`, trechos de bootstrap/seed do guia de reprodução histórico. Consulta pontual aos gates de ativação de `telemetry.go` e `telemetry.py`; a revisão completa de aplicações pertence ao relatório paralelo.

## 7. Lista de encerramento para a revisão principal

- [ ] Confirmar conta/backend/identidade/região/cotas/orçamento e parâmetros reais.
- [ ] Publicar imagens/configurações mediante fluxo autorizado; substituir todas as sentinelas.
- [ ] Atualizar runbook do 04 incluindo ArgoCD em duas etapas, schemas e seed da chave.
- [ ] Implantar e testar funcionalmente a base no cluster.
- [ ] Acrescentar charts/configurações de Collector, Prometheus, Loki e Grafana ao GitOps.
- [ ] Ativar OTel nos cinco workloads e implementar os três sinais/destinos.
- [ ] Comprovar APM/trace/Service Map e dashboard customizado.
- [ ] Implementar alerta → incidente/acionamento → ChatOps → mitigação e verificação de recuperação.
- [ ] Executar CI/DevSecOps final, revisar exceções datadas e incorporar a regressão OTel ao CI como melhoria técnica.
- [ ] Capturar evidências de runtime e entrega; revisão estática não encerra REQ-OBR-23.

Estado para o próximo agente: nenhuma correção aplicada neste relatório. Fonte para a matriz principal e backlog, sem substituir decisões de arquitetura, sem converter propostas de três nós ou gates adicionais em exigências da FIAP.
