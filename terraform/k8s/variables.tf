# ============================================================
# VARIAVEIS DE ENTRADA - camada k8s
# ============================================================

variable "aws_region" {
  description = "Regiao AWS. Precisa ser a mesma das outras camadas (F-012)."
  type        = string
  default     = "us-east-2"
}

variable "expected_aws_account_id" {
  description = "ID confirmado da NOVA conta AWS da Fase 4. O provider recusa credenciais de outra conta."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[0-9]{12}$", var.expected_aws_account_id))
    error_message = "Informe o ID real da nova conta AWS, com 12 digitos."
  }
}

variable "state_bucket" {
  description = "Bucket novo e exclusivo do estado da Fase 4; deve coincidir com backend.hcl. Nunca reutilizar o estado da Fase 3."
  type        = string
  nullable    = false

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.state_bucket))
    error_message = "Informe o nome real do bucket S3 criado para a Fase 4."
  }
}

variable "state_region" {
  description = "Regiao do bucket de estado da Fase 4; deve coincidir com backend.hcl."
  type        = string
  nullable    = false
}

variable "base_state_key" {
  description = "Chave da base da Fase 4 no bucket de estado."
  type        = string
  default     = "phase4/prod/base.tfstate"
}

variable "cluster_state_key" {
  description = "Chave da camada cluster da Fase 4 no bucket de estado."
  type        = string
  default     = "phase4/prod/cluster.tfstate"
}

variable "project_name" {
  description = "Prefixo dos nomes. Mesmo valor das outras camadas."
  type        = string
  default     = "togglemaster"
}

variable "default_tags" {
  description = "Tags aplicadas a todo recurso AWS desta camada (D-009), em minusculas."
  type        = map(string)
  default = {
    project = "fiap"
    phase   = "4"
  }
}

variable "app_namespace" {
  description = <<-EOT
    Namespace das aplicacoes. Precisa bater com o declarado em
    gitops/base/kustomization.yaml e com o usado nas politicas de
    confianca do IRSA - hoje "togglemaster" (F-019).
  EOT
  type        = string
  default     = "togglemaster"
}

# ------------------------------------------------------------
# ArgoCD
# ------------------------------------------------------------

variable "argocd_namespace" {
  description = "Namespace do ArgoCD. Separado do das aplicacoes, como o chart oficial recomenda."
  type        = string
  default     = "argocd"
}

variable "argocd_chart_version" {
  description = <<-EOT
    Versao do chart argo-cd do repositorio argoproj/argo-helm.

    FIXA de proposito: com a versao em aberto, um apply feito na semana
    da gravacao poderia trazer uma release nova e mudar o comportamento
    sem ninguem pedir.

    7.7.23 e o ultimo chart da linha 7.7 (Argo CD 2.13). Sozinho ele
    instalaria a v2.13.4; a imagem corrigida vem de argocd_image_tag.
  EOT
  type        = string
  default     = "7.7.23"
}

variable "argocd_image_tag" {
  description = <<-EOT
    Tag da imagem do Argo CD usada por todos os componentes do chart
    (values global.image.tag).

    v2.13.9 corrige a CVE-2025-55190 (critica: um token de projeto podia
    ler as credenciais de repositorio). Nenhum chart da linha 7.7 traz
    essa versao, e as linhas 3.x mudam a configuracao. Por isso o chart
    fica no 7.7.23 e so a imagem sobe. A v2.13.9 embute o mesmo helm
    3.15.4 e o mesmo kustomize 5.4.3 da v2.13.2, entao a renderizacao dos
    charts da observabilidade nao muda.
  EOT
  type        = string
  default     = "v2.13.9"
}

variable "gitops_repo_url" {
  description = <<-EOT
    Repositorio que o ArgoCD observa (O-25). E o proprio monorepo: a
    area GitOps e a pasta gitops/, conforme o enunciado permite
    (O-22 e R-07).
  EOT
  type        = string
  default     = "https://github.com/fiap-devops-arqcloud-2026/tech-challenge-04.git"
}

variable "gitops_repo_path" {
  description = "Pasta observada dentro do repositorio. E o overlay do unico ambiente (D-011)."
  type        = string
  default     = "gitops/overlays/prod"
}

variable "gitops_repo_branch" {
  description = <<-EOT
    Branch de publicacao futura: main. O trabalho atual ocorre somente
    na dev, sem publicacao ou sincronizacao do cluster. A main precisa
    receber um PR aprovado antes de este caminho existir no remoto.
  EOT
  type        = string
  default     = "main"
}

# Token somente se o repositorio 04 for privado. Nunca copiar tokens do 03.
variable "github_token" {
  description = <<-EOT
    Credencial de leitura do repositorio tech-challenge-04 para ArgoCD,
    somente se ele for privado; a visibilidade atual nao foi verificada
    nesta importacao. Fine-grained token com Contents: Read-only e acesso
    ao repositorio 04, com Resource owner da organizacao correspondente.
    Informar por TF_VAR_github_token, sem valor em arquivo versionado.
    Deixar vazio se publico: nesse caso o Secret de repositorio nao nasce.
  EOT
  type        = string
  default     = ""
  # Impede que o valor apareca no plan, no apply e nos outputs.
  sensitive = true
}

# ------------------------------------------------------------
# Armazenamento
# ------------------------------------------------------------

variable "storage_class_name" {
  description = <<-EOT
    Nome da StorageClass padrao criada por esta camada.

    Precisa ser IDENTICO ao storageClassName declarado no
    volumeClaimTemplates de gitops/base/postgres-targeting/statefulset.yaml.
    Divergencia deixa o PVC em Pending para sempre - foi o que travou a
    Fase 2 (F-025).
  EOT
  type        = string
  default     = "gp3"
}

# ------------------------------------------------------------
# Observabilidade (Fase 4) - segredos das integracoes SaaS
# ------------------------------------------------------------
# Os quatro valores abaixo viram Secrets do Kubernetes no namespace
# observability (observability.tf). Nenhum tem default: o apply nao
# deve acontecer sem eles. Informar por TF_VAR_<nome>, a partir do .env
# local (ignorado pelo Git); nunca escrever em arquivo versionado.
# ------------------------------------------------------------

variable "new_relic_license_key" {
  description = "License key de ingestao do New Relic (tipo Ingest - License, 40 caracteres). Usada pelo Collector gateway no header api-key do exporter otlp_http."
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.new_relic_license_key) == 40
    error_message = "A license key de ingestao do New Relic tem 40 caracteres."
  }
}

variable "pagerduty_integration_key" {
  description = "Integration Key (32 caracteres) da integracao Events API V2 do servico ToggleMaster Fase 4 no PagerDuty. Usada pelo contact point PagerDuty do Grafana."
  type        = string
  sensitive   = true

  validation {
    condition     = can(regex("^[0-9a-zA-Z]{32}$", var.pagerduty_integration_key))
    error_message = "A Integration Key do PagerDuty tem 32 caracteres alfanumericos."
  }

  # O Grafana troca $PAGERDUTY_INTEGRATION_KEY pelo valor e, se ele parecer
  # um numero (so digitos, ou digitos com um "e"), guarda como numero e o
  # provisionamento falha. Testado em 2026-11-03 no Grafana 13.3.0. Nesse
  # caso raro, recriar a integracao Events API V2 gera uma chave nova.
  validation {
    condition     = !can(tonumber(var.pagerduty_integration_key))
    error_message = "Esta Integration Key seria lida como numero pelo Grafana. Recrie a integracao Events API V2 no PagerDuty para obter outra chave."
  }
}

variable "slack_webhook_url" {
  description = "URL do Incoming Webhook do canal de incidentes no Slack. A URL e o proprio segredo. Usada pelo contact point Slack do Grafana."
  type        = string
  sensitive   = true

  validation {
    condition     = startswith(var.slack_webhook_url, "https://hooks.slack.com/services/")
    error_message = "A URL do webhook do Slack comeca com https://hooks.slack.com/services/."
  }
}

variable "github_dispatch_token" {
  description = "Fine-grained token do GitHub, restrito ao repositorio tech-challenge-04, que o Grafana usa para chamar a API repository_dispatch e disparar o workflow self-healing.yml. Diferente do github_token de leitura do ArgoCD."
  type        = string
  sensitive   = true

  validation {
    # Fine-grained (github_pat_) e o recomendado; o classico (ghp_, escopo
    # repo) tambem funciona na API repository_dispatch.
    condition     = startswith(var.github_dispatch_token, "github_pat_") || startswith(var.github_dispatch_token, "ghp_")
    error_message = "Informe por TF_VAR_github_dispatch_token um token do GitHub (fine-grained github_pat_ ou classico ghp_)."
  }
}

variable "observability_namespace" {
  description = "Namespace da stack de observabilidade (Prometheus, Grafana, Loki e Collectors). Precisa ser o mesmo dos manifestos de gitops/observability e do endpoint OTEL dos servicos."
  type        = string
  default     = "observability"
}
