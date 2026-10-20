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
  EOT
  type        = string
  default     = "7.7.11"
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
